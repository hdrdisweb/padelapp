from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Para usar AUTH_USER_MODEL
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User


# Modelo de Usuario
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    dni_nie = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])
    movil = models.CharField(max_length=15, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    poblacion = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    apodo = models.CharField(max_length=50, blank=True, null=True)
    posicion_juego = models.CharField(max_length=10, choices=[('Izquierda', 'Izquierda'), ('Derecha', 'Derecha'), ('Ambas', 'Ambas')])
    marca_pala = models.CharField(max_length=100, blank=True, null=True)
    equipo = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='jugadores')

    def __str__(self):
        return self.username
    
    # Modelo de Pull (Partidos abiertos para inscribirse)
class Pull(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=True, blank=True)
    pull_asociada = models.ForeignKey('CrearPull', on_delete=models.CASCADE, null=True, blank=True)
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pulls_inscritos')
    tipo = models.CharField(max_length=20, choices=[('Titular', 'Titular'), ('Reserva', 'Reserva'), ('No puedo asistir', 'No puedo asistir')])
    timestamp = models.DateTimeField(auto_now_add=True)
    max_jugadores = models.IntegerField(default=12)

    # Aquí colocamos la función __str__
    def __str__(self):
        if self.match:
            return f"{self.jugador.username} - {self.tipo} en {self.match.ubicacion}"
        elif hasattr(self, 'pull_asociada') and self.pull_asociada:
            return f"{self.jugador.username} - {self.tipo} en Pull: {self.pull_asociada.nombre}"
        else:
            return f"{self.jugador.username} - {self.tipo} (sin ubicación)"



# Modelo de Convocatoria LAPA
class LapaMatch(models.Model):
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lapa_partidos_creados')
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Confirmado', 'Confirmado'), ('Cancelado', 'Cancelado')], default="Pendiente")
    motivo_cancelacion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"LAPA en {self.ubicacion} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

# Modelo de Inscripción en LAPA
class LapaPull(models.Model):
    match = models.ForeignKey(LapaMatch, on_delete=models.CASCADE, related_name='lapa_pulls')
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lapa_pulls_inscritos')
    tipo = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('No disponible', 'No disponible')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.jugador.username} - {self.tipo} en {self.match.ubicacion}"

# Modelo de Convocatoria SNP
class SnpMatch(models.Model):
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='snp_partidos_creados')
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Confirmado', 'Confirmado'), ('Cancelado', 'Cancelado')], default="Pendiente")
    motivo_cancelacion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"SNP en {self.ubicacion} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

# Modelo de Inscripción en SNP
class SnpPull(models.Model):
    match = models.ForeignKey(SnpMatch, on_delete=models.CASCADE, related_name='snp_pulls')
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='snp_pulls_inscritos')
    tipo = models.CharField(max_length=20, choices=[('Disponible', 'Disponible'), ('No disponible', 'No disponible')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.jugador.username} - {self.tipo} en {self.match.ubicacion}"

# Historial de partidos
class MatchHistory(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="match_history")
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=[("win", "Victoria"), ("loss", "Derrota")])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.match} - {self.result}"

# Notificaciones
class Notification(models.Model):
    TYPE_CHOICES = [
        ('pull', 'Inscripción en una Pull'),
        ('match', 'Inscripción en un Partido'),
        ('full_match', 'Partido Completo'),
        ('removed', 'Eliminación de Partido/Pull'),
        ('message', 'Mensaje Importante'),
        ('admin_summary', 'Resumen para Administrador'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    is_admin_notification = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.message}"

    @classmethod
    def send_admin_summary(cls):
        last_hour = now() - timedelta(hours=1)
        count = Notification.objects.filter(notification_type="match", created_at__gte=last_hour).count()
        
        if count > 0:
            admin = User.objects.filter(is_superuser=True).first()
            if admin:
                cls.objects.create(
                    user=admin,
                    notification_type="admin_summary",
                    message=f"{count} jugadores se han apuntado en la última hora.",
                    send_email=True,
                    is_admin_notification=True
                )

# Perfil de usuario para configurar notificaciones
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receive_individual_notifications = models.BooleanField(default=False)

#creacion de pull

class CrearPull(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    max_jugadores = models.IntegerField(default=12)

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"


class Match(models.Model):
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches')
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    estado = models.CharField(max_length=10, choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], default='Abierto')

    def __str__(self):
        return f"Match en {self.lugar} - {self.fecha}"


# Modelo de partidos

class PartidoAbierto(models.Model):
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partidos_creados'
    )
    jugadores = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='partidos_jugados', blank=True
    )
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=10, choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], default='Abierto'
    )

    def save(self, *args, **kwargs):
        """Asegura que el estado se actualiza solo si el objeto ya tiene ID."""
        if self.pk:
            if self.jugadores.count() >= 4:
                self.estado = 'Cerrado'
            else:
                self.estado = 'Abierto'

        super().save(*args, **kwargs)

    @classmethod
    def limpiar_partidos_viejos(cls):
        """Elimina partidos cerrados que tengan más de 1 día."""
        cls.objects.filter(estado='Cerrado', fecha__lt=now() - timedelta(days=1)).delete()


def save(self, *args, **kwargs):
    """Asegura que el estado se actualiza solo si el objeto ya tiene ID."""
    if self.pk:  # ✅ Solo ejecuta la validación si el objeto ya tiene un ID
        if self.jugadores.count() >= 4:
            self.estado = 'Cerrado'
        else:
            self.estado = 'Abierto'

    # Llamamos a la función original después de modificar el estado
    super().save(*args, **kwargs)


    def __str__(self):
        return f"Partido en {self.lugar} el {self.fecha} a las {self.hora} - {self.estado}"


    @classmethod
    def limpiar_partidos_viejos(cls):
        cls.objects.filter(estado='Cerrado', fecha__lt=now() - timedelta(days=1)).delete()


# Modelo de Pareja (una pareja de dos jugadores)
class Pareja(models.Model):
    jugador_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pareja_j1')
    jugador_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pareja_j2')

    def __str__(self):
        return f"{self.jugador_1.apodo or self.jugador_1.username} / {self.jugador_2.apodo or self.jugador_2.username}"

# Modelo de Alineación (por Pull)
class Alineacion(models.Model):
    pull = models.OneToOneField(CrearPull, on_delete=models.CASCADE, related_name='alineacion')
    parejas = models.ManyToManyField(Pareja, through='ParejaEnPista')
    suplentes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='suplente_en_alineaciones')
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alineación para {self.pull.nombre}"

# Relación entre Pareja y pista asignada
class ParejaEnPista(models.Model):
    alineacion = models.ForeignKey(Alineacion, on_delete=models.CASCADE)
    pareja = models.ForeignKey(Pareja, on_delete=models.CASCADE)
    pista = models.PositiveSmallIntegerField()  # Pista 1, 2, 3...

    class Meta:
        unique_together = ('alineacion', 'pareja')
        ordering = ['pista']


# Modelo de Equipo
class Team(models.Model):
    TIPO_CONVOCATORIA = [
        ('LAPA 3', 'LAPA 3'),
        ('LAPA 4', 'LAPA 4'),
        ('SNP 500', 'SNP 500'),
        ('SNP 1000', 'SNP 1000'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CONVOCATORIA)

    def __str__(self):
        return self.nombre



# convocatorias

class Convocatoria(models.Model):
    equipo = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='convocatorias')
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipo.tipo} - {self.equipo.nombre} ({self.fecha})"


class ConvocatoriaJugador(models.Model):
    TIPO_RESPUESTA = [
        ('PUEDO', 'PUEDO'),
        ('NO PUEDO', 'NO PUEDO'),
    ]

    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='jugadores_convocados')
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=10, choices=TIPO_RESPUESTA, blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('convocatoria', 'jugador')

    def __str__(self):
        return f"{self.jugador.username} en {self.convocatoria} - {self.respuesta or 'Sin respuesta'}"


class ConvocatoriaPareja(models.Model):
    jugador_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convocatoria_pareja_j1')
    jugador_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convocatoria_pareja_j2')

    def __str__(self):
        return f"{self.jugador_1.username} / {self.jugador_2.username}"

class ParejaEnPistaConvocatoria(models.Model):
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='pistas')
    pareja = models.ForeignKey(ConvocatoriaPareja, on_delete=models.CASCADE)
    pista = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('convocatoria', 'pareja')
        ordering = ['pista']

# convocatorias lapa y snp

class AlineacionConvocatoria(models.Model):
    convocatoria = models.OneToOneField('Convocatoria', on_delete=models.CASCADE, related_name='alineacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alineación de {self.convocatoria}"


class ParejaConvocatoria(models.Model):
    alineacion = models.ForeignKey(AlineacionConvocatoria, on_delete=models.CASCADE, related_name='parejas')
    jugador_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pareja_conv_j1')
    jugador_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pareja_conv_j2')
    pista = models.IntegerField()

    def __str__(self):
        return f"Pista {self.pista}: {self.jugador_1} y {self.jugador_2}"


class SuplenteConvocatoria(models.Model):
    alineacion = models.ForeignKey(AlineacionConvocatoria, on_delete=models.CASCADE, related_name='suplentes')
    jugador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Suplente: {self.jugador}"
