# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PadelappAlineacion(models.Model):
    creada_por = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    pull = models.OneToOneField('PadelappCrearpull', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_alineacion'


class PadelappAlineacionSuplentes(models.Model):
    alineacion = models.ForeignKey(PadelappAlineacion, models.DO_NOTHING)
    user = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_alineacion_suplentes'
        unique_together = (('alineacion', 'user'),)


class PadelappCrearpull(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    max_jugadores = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'padelapp_crearpull'


class PadelappLapamatch(models.Model):
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20)
    motivo_cancelacion = models.TextField(blank=True, null=True)
    creador = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_lapamatch'


class PadelappLapapull(models.Model):
    tipo = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    jugador = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    match = models.ForeignKey(PadelappLapamatch, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_lapapull'


class PadelappMatch(models.Model):
    fecha = models.DateTimeField()
    creador = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    lugar = models.CharField(max_length=200)
    estado = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'padelapp_match'


class PadelappMatchhistory(models.Model):
    result = models.CharField(max_length=10)
    date = models.DateTimeField()
    match = models.ForeignKey(PadelappMatch, models.DO_NOTHING)
    player = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_matchhistory'


class PadelappNotification(models.Model):
    notification_type = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField()
    is_read = models.BooleanField()
    send_email = models.BooleanField()
    is_admin_notification = models.BooleanField()
    user = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_notification'


class PadelappPareja(models.Model):
    jugador_1 = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    jugador_2 = models.ForeignKey('PadelappUser', models.DO_NOTHING, related_name='padelapppareja_jugador_2_set')

    class Meta:
        managed = False
        db_table = 'padelapp_pareja'


class PadelappParejaenpista(models.Model):
    pista = models.PositiveSmallIntegerField()
    alineacion = models.ForeignKey(PadelappAlineacion, models.DO_NOTHING)
    pareja = models.ForeignKey(PadelappPareja, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_parejaenpista'
        unique_together = (('alineacion', 'pareja'),)


class PadelappPartidoabierto(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)
    estado = models.CharField(max_length=10)
    creador = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_partidoabierto'


class PadelappPartidoabiertoJugadores(models.Model):
    partidoabierto = models.ForeignKey(PadelappPartidoabierto, models.DO_NOTHING)
    user = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_partidoabierto_jugadores'
        unique_together = (('partidoabierto', 'user'),)


class PadelappPull(models.Model):
    tipo = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    max_jugadores = models.IntegerField()
    jugador = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    match = models.ForeignKey(PadelappMatch, models.DO_NOTHING, blank=True, null=True)
    pull_asociada = models.ForeignKey(PadelappCrearpull, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padelapp_pull'


class PadelappSnpmatch(models.Model):
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20)
    motivo_cancelacion = models.TextField(blank=True, null=True)
    creador = models.ForeignKey('PadelappUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_snpmatch'


class PadelappSnppull(models.Model):
    tipo = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    jugador = models.ForeignKey('PadelappUser', models.DO_NOTHING)
    match = models.ForeignKey(PadelappSnpmatch, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_snppull'


class PadelappTeam(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'padelapp_team'


class PadelappUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    avatar = models.CharField(max_length=100, blank=True, null=True)
    dni_nie = models.CharField(unique=True, max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10)
    movil = models.CharField(max_length=15, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    poblacion = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    apodo = models.CharField(max_length=50, blank=True, null=True)
    posicion_juego = models.CharField(max_length=10)
    marca_pala = models.CharField(max_length=100, blank=True, null=True)
    equipo = models.ForeignKey(PadelappTeam, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'padelapp_user'


class PadelappUserGroups(models.Model):
    user = models.ForeignKey(PadelappUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_user_groups'
        unique_together = (('user', 'group'),)


class PadelappUserUserPermissions(models.Model):
    user = models.ForeignKey(PadelappUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_user_user_permissions'
        unique_together = (('user', 'permission'),)


class PadelappUserprofile(models.Model):
    receive_individual_notifications = models.BooleanField()
    user = models.OneToOneField(PadelappUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padelapp_userprofile'
