import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Match, Pull, Notification, CrearPull  # Importar desde padelapp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import IntegrityError
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from .models import PartidoAbierto
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
from .models import Alineacion, Pareja, ParejaEnPista
from django.contrib.auth import get_user_model
from django.urls import reverse






@login_required
def inscribir_a_partido(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    user = request.user

    if match.players.filter(id=user.id).exists():
        return JsonResponse({'error': 'Ya estás inscrito en este partido'}, status=400)

    match.players.add(user)

    Notification.objects.create(
        user=user,
        notification_type="match",
        message=f"Te has inscrito en el partido {match}.",
    )

    return JsonResponse({'success': 'Inscripción realizada con éxito'})

@login_required
def inscribir_a_pull(request, pull_id):
    pull = get_object_or_404(Pull, id=pull_id)
    user = request.user

    if Pull.objects.filter(jugador=user, match=pull.match).exists():
        return JsonResponse({'error': 'Ya estás inscrito en este pull'}, status=400)

    pull.jugador = user
    pull.save()

    Notification.objects.create(
        user=user,
        notification_type="pull",
        message=f"Te has inscrito en una pull para el partido {pull.match}.",
    )

    return JsonResponse({'success': 'Inscripción en pull realizada con éxito'})


# creamos, editamos PULL
# Solo los administradores pueden crear pulls
def es_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(es_admin)
def crear_pull(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        max_jugadores = int(request.POST['max_jugadores'])

        # Creamos la pull usando el nuevo modelo CrearPull
        nueva_pull = CrearPull(nombre=nombre, fecha=fecha, hora=hora, max_jugadores=max_jugadores)
        nueva_pull.save()

        messages.success(request, 'Pull creada correctamente.')
        request.session.pop('_messages', None)
        return render(request, 'padelapp/pull_form.html')


    
    return render(request, 'padelapp/pull_form.html')

def lista_pulls(request):
    pulls = CrearPull.objects.all()
    return render(request, 'padelapp/lista_pulls.html', {'pulls': pulls})

def detalle_pull(request, id):
    pull = get_object_or_404(CrearPull, id=id)

    # Inscripciones
    inscritos = Pull.objects.filter(pull_asociada=pull)
    titulares = inscritos.filter(tipo='Titular')
    reservas = inscritos.filter(tipo='Reserva')
    no_asisten = inscritos.filter(tipo='No puedo asistir')

    # 🔗 Generar link para compartir por WhatsApp
    pull_url = request.build_absolute_uri(reverse('detalle_pull', args=[pull.id]))
    mensaje_whatsapp = f"¡Nueva pull creada! 🎾\n\nPull: {pull.nombre}\n🗓️ {pull.fecha} ⏰ {pull.hora}\n\n👉 Inscribite: {pull_url}"

    return render(request, 'padelapp/detalle_estado_pull.html', {
        'pull': pull,
        'titulares': titulares,
        'reservas': reservas,
        'no_asisten': no_asisten,
        'mensaje_whatsapp': mensaje_whatsapp,
    })


#def detalle_pull(request, id):
    pull = get_object_or_404(CrearPull, id=id)
    return render(request, 'padelapp/detalle_pull.html', {'pull': pull})



def editar_pull(request, id):
    pull = get_object_or_404(CrearPull, id=id)
    
    if request.method == 'POST':
        pull.nombre = request.POST['nombre']
        pull.fecha = request.POST['fecha']
        pull.hora = request.POST['hora']
        pull.max_jugadores = int(request.POST['max_jugadores'])
        pull.save()
        return redirect('lista_pulls')

    return render(request, 'padelapp/pull_form.html', {'pull': pull})

def eliminar_pull(request, id):
    pull = get_object_or_404(CrearPull, id=id)
    
    if request.method == 'POST':
        pull.delete()
        messages.success(request, 'Pull eliminada con éxito.')
        return redirect('lista_pulls')
    
    return render(request, 'padelapp/confirmar_eliminar.html', {'pull': pull})

# Inscribirse a las pull
@login_required
def inscribirse_pull(request, id):
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        pull = get_object_or_404(CrearPull, id=id)
        user = request.user

        print(f"📌 {user.username} intenta inscribirse en la Pull {pull.nombre} como {tipo}")

        if tipo == "Titular" and Pull.objects.filter(pull_asociada=pull, tipo="Titular").count() >= pull.max_jugadores:
            messages.error(request, "La lista de titulares ya está llena. Elige otra opción.")
            return redirect("detalle_pull", pk=pull.id)

        inscripcion, created = Pull.objects.update_or_create(
            jugador=user,
            pull_asociada=pull,
            defaults={'tipo': tipo}
        )

        if created:
            messages.success(request, f"Te has inscrito como {tipo} en {pull.nombre}")
            print(f"✅ Inscripción creada: {inscripcion}")

            # 📌 Crear la notificación asegurando que `is_read=False`
            notificacion = Notification.objects.create(
                user=user,
                notification_type="pull",
                message=f"Te has inscrito en la Pull {pull.nombre} para el {pull.fecha} a las {pull.hora}.",
                is_read=False  # 🔹 IMPORTANTE: Asegurar que no se marque como leída
            )
            print(f"🟢 Notificación creada: {notificacion}")

        else:
            messages.success(request, f"Tu inscripción ha sido actualizada a {tipo}")
            print(f"♻️ Inscripción actualizada: {inscripcion}")

        if Pull.objects.filter(pull_asociada=pull, tipo="Titular").count() == pull.max_jugadores:
            for jugador in Pull.objects.filter(pull_asociada=pull).values_list('jugador', flat=True):
                notificacion_full_pull = Notification.objects.create(
                    user_id=jugador,
                    notification_type="full_pull",
                    message=f"La Pull {pull.nombre} para el {pull.fecha} a las {pull.hora} está completa.",
                    is_read=False  # 🔹 Asegurar que no se marque como leída
                )
                print(f"🔴 Notificación de Pull llena creada: {notificacion_full_pull}")

        return redirect("lista_pulls")


# salir pulls

@login_required
def salir_pull(request, id):
    pull = get_object_or_404(CrearPull, id=id)
    user = request.user

    # Verificar si el usuario estaba inscrito
    inscripcion = Pull.objects.filter(jugador=user, pull_asociada=pull).first()
    
    if inscripcion:
        inscripcion.delete()
        messages.info(request, f"Has salido de la Pull {pull.nombre}.")
        print(f"🚨 {user.username} ha salido de la Pull {pull.nombre}")

        # 📌 Notificación para el usuario que salió
        Notification.objects.create(
            user=user,
            notification_type="removed_pull",
            message=f"Has salido de la Pull {pull.nombre} para el {pull.fecha} a las {pull.hora}.",
        )

        # 📌 Notificación para los demás jugadores avisando que hay un cupo disponible
        for jugador in Pull.objects.filter(pull_asociada=pull).values_list('jugador', flat=True):
            Notification.objects.create(
                user_id=jugador,
                notification_type="pull",
                message=f"{user.username} ha salido de la Pull {pull.nombre}, hay una plaza disponible.",
            )

    return redirect("lista_pulls")



# Modelo para los partidos 

# 🔹 Función para verificar si el usuario es administrador
def es_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def crear_partido(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')  
        lugar = request.POST.get('lugar')

        if fecha and hora and lugar:
            # ✅ Primero creamos y guardamos el partido
            partido = PartidoAbierto.objects.create(
                creador=request.user,
                fecha=fecha,
                hora=hora,
                lugar=lugar,
                estado='Abierto'
            )

            # ✅ Ahora, inscribimos automáticamente al creador
            partido.jugadores.add(request.user)

            messages.success(request, '¡Partido creado! Te has unido automáticamente.')
            return redirect('lista_partidos')

    return render(request, 'padelapp/crear_partido.html')




# listar los partidos 

def lista_partidos(request):
    PartidoAbierto.limpiar_partidos_viejos()
    partidos = PartidoAbierto.objects.all().order_by('-fecha')

    for partido in partidos:
        url = request.build_absolute_uri(reverse('gestionar_partido', args=[partido.id]))
        partido.mensaje_whatsapp = f"🎾 ¡Sumate al partido en {partido.lugar}!\n🗓️ {partido.fecha} ⏰ {partido.hora}\n👉 {url}"

    return render(request, 'padelapp/lista_partidos.html', {'partidos': partidos})

# gestionar partidos

@login_required
def gestionar_partido(request, partido_id):
    partido = get_object_or_404(PartidoAbierto, id=partido_id)

    if request.user in partido.jugadores.all():
        partido.jugadores.remove(request.user)
        messages.info(request, 'Has salido del partido. Ahora hay una plaza libre.')
    else:
        if partido.jugadores.count() < 4:
            partido.jugadores.add(request.user)
            messages.success(request, '¡Te has unido al partido!')
        else:
            messages.error(request, 'El partido ya está completo.')

    partido.save()
    return redirect('lista_partidos')

# Notificaciones
@login_required
def get_notifications(request):
    """Devuelve todas las notificaciones no leídas del usuario"""
    notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
    data = [
        {
            "id": n.id,
            "type": n.notification_type,
            "message": n.message,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for n in notifications
    ]
    return JsonResponse({"notifications": data, "count": notifications.count()})


# Marva las notificaciones como leidas
@csrf_exempt
@login_required
def mark_notifications_as_read(request):
    """Marcar todas las notificaciones del usuario como leídas"""
    if request.method != "POST":
        return JsonResponse({"error": f"Método no permitido: {request.method}"}, status=405)

    print(f"🔍 Se están marcando como leídas para {request.user.username}")

    notificaciones_no_leidas = request.user.notifications.filter(is_read=False)

    if notificaciones_no_leidas.exists():
        notificaciones_no_leidas.update(is_read=True)  # 🔹 Marcar como leídas solo cuando el usuario haga clic
        print(f"✅ Notificaciones marcadas como leídas para {request.user.username}")
        return JsonResponse({"success": True, "count": 0})

    print(f"⚠️ No había notificaciones pendientes para {request.user.username}")
    return JsonResponse({"success": True, "count": 0})


    # 📌 Notificación para el usuario que se inscribió
    Notification.objects.create(
        user=user,
        notification_type="match",
        message=f"Te has unido al partido en {partido.lugar} el {partido.fecha}.",
    )

    # 📌 Si el partido se completa con 4 jugadores, enviar notificación a todos
    if partido.jugadores.count() == 4:
        for jugador in partido.jugadores.all():
            Notification.objects.create(
                user=jugador,
                notification_type="full_match",
                message=f"El partido en {partido.lugar} el {partido.fecha} ahora está completo.",
            )

    partido.save()
    return JsonResponse({'success': 'Te has unido al partido', 'players': partido.jugadores.count()})


# informar a los demas que hay un cupo libre

@login_required
def gestionar_partido(request, partido_id):
    partido = get_object_or_404(PartidoAbierto, id=partido_id)
    user = request.user

    if user in partido.jugadores.all():
        partido.jugadores.remove(user)
        messages.info(request, 'Has salido del partido. Ahora hay una plaza libre.')

        # 📌 Notificación para el usuario que salió
        Notification.objects.create(
            user=user,
            notification_type="removed",
            message=f"Has salido del partido en {partido.lugar} el {partido.fecha}.",
        )

        # 📌 Notificación para los demás jugadores
        for jugador in partido.jugadores.all():
            Notification.objects.create(
                user=jugador,
                notification_type="match",
                message=f"{user.username} ha salido del partido en {partido.lugar}, vuelve a haber un cupo disponible.",
            )
    else:
        if partido.jugadores.count() < 4:
            partido.jugadores.add(user)
            messages.success(request, '¡Te has unido al partido!')
            
            Notification.objects.create(
                user=user,
                notification_type="match",
                message=f"Te has unido al partido en {partido.lugar} el {partido.fecha}.",
            )

    partido.save()
    return redirect('lista_partidos')

#lista notificaciones
@login_required
def lista_notificaciones(request):
    """Muestra todas las notificaciones del usuario"""
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'padelapp/notificaciones.html', {'notifications': notifications})

# gestionar las alineaciones

User = get_user_model()

@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
@login_required
def gestionar_alineacion(request, pull_id):
    pull = get_object_or_404(CrearPull, id=pull_id)
    inscritos = Pull.objects.filter(pull_asociada=pull, tipo='Titular').select_related('jugador')
    jugadores = [p.jugador for p in inscritos]
    alineacion = Alineacion.objects.filter(pull=pull).first()

    if request.method == "POST":
        data_json = request.POST.get('alineacion_data')
        print("🔍 DATA RECIBIDA:", data_json)

        if data_json:
            data = json.loads(data_json)
            parejas_data = data.get('parejas', [])
            suplentes_ids = data.get('suplentes', [])

            if alineacion:
                alineacion.parejas.clear()
                alineacion.suplentes.clear()
                ParejaEnPista.objects.filter(alineacion=alineacion).delete()
            else:
                alineacion = Alineacion.objects.create(pull=pull, creada_por=request.user)

            for pareja_info in parejas_data:
                jugador1 = User.objects.get(id=pareja_info['jugador1'])
                jugador2 = User.objects.get(id=pareja_info['jugador2'])
                pista = int(pareja_info['pista'])

                pareja = Pareja.objects.create(jugador_1=jugador1, jugador_2=jugador2)
                ParejaEnPista.objects.create(alineacion=alineacion, pareja=pareja, pista=pista)

            suplentes = User.objects.filter(id__in=suplentes_ids)
            alineacion.suplentes.set(suplentes)

            messages.success(request, "Alineación guardada correctamente.")
            return redirect('gestionar_alineacion', pull_id=pull.id)

    # Cargar parejas guardadas para mostrar en las pistas
    parejas_en_pista = None
    jugadores_asignados = []
    if alineacion:
        parejas_en_pista = ParejaEnPista.objects.filter(alineacion=alineacion).select_related('pareja')
        for item in parejas_en_pista:
            jugadores_asignados.append(item.pareja.jugador_1)
            jugadores_asignados.append(item.pareja.jugador_2)

    # Mostrar solo los jugadores no asignados
    jugadores_disponibles = [j for j in jugadores if j not in jugadores_asignados]

    alineacion_url = request.build_absolute_uri(reverse('gestionar_alineacion', args=[pull.id]))
    mensaje_whatsapp = f"¡Mirá la alineación de {pull.nombre}! 👉 {alineacion_url}"


    context = {
        'pull': pull,
        'jugadores': jugadores_disponibles,
        'alineacion': alineacion,
        'parejas_en_pista': parejas_en_pista,
        'mensaje_whatsapp': mensaje_whatsapp,
    }
    return render(request, 'padelapp/gestionar_alineacion.html', context)
