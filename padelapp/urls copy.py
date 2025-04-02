from django.urls import path
from .views import inscribir_a_partido, inscribir_a_pull
from . import views
from .views import crear_partido, gestionar_partido, lista_partidos
from .views import get_notifications, mark_notifications_as_read, lista_notificaciones, salir_pull
from .views import crear_convocatoria, detalle_convocatoria, editar_convocatoria, eliminar_convocatoria
from .views import editar_equipo






urlpatterns = [
    path("inscribir/partido/<int:match_id>/", inscribir_a_partido, name="inscribir_a_partido"),
    # path("inscribir/pull/<int:pull_id>/", inscribir_a_pull, name="inscribir_a_pull"),
    path('crear_pull/', views.crear_pull, name='crear_pull'),
    path('lista_pulls/', views.lista_pulls, name='lista_pulls'),
    path('pull/<int:id>/', views.detalle_pull, name='detalle_pull'),
    path('pull/<int:id>/editar/', views.editar_pull, name='editar_pull'),
    path('pull/<int:id>/eliminar/', views.eliminar_pull, name='eliminar_pull'),
    path('pull/<int:id>/inscribirse/', views.inscribirse_pull, name='inscribirse_pull'),
    path('partidos/', lista_partidos, name='lista_partidos'),
    path('partidos/crear/', crear_partido, name='crear_partido'),
    path('partidos/<int:partido_id>/gestionar/', gestionar_partido, name='gestionar_partido'),
    path('partidos/<int:partido_id>/eliminar/', views.eliminar_partido, name='eliminar_partido'),
    path('notifications/', get_notifications, name='get_notifications'),
    path('notifications/read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path("notificaciones/", lista_notificaciones, name="lista_notificaciones"),
    path('pull/<int:id>/salir/', salir_pull, name='salir_pull'),
    path('pull/<int:pull_id>/alineacion/', views.gestionar_alineacion, name='gestionar_alineacion'),
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipo/<int:id>/', views.detalle_equipo, name='detalle_equipo'),
    path('equipo/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipo/<int:equipo_id>/editar/', editar_equipo, name='editar_equipo'),
    path('equipo/<int:id>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    path('convocatorias/nueva/', crear_convocatoria, name='crear_convocatoria'),
    path('convocatorias/<int:pk>/', detalle_convocatoria, name='detalle_convocatoria'),
    path('convocatorias/', views.lista_convocatorias, name='lista_convocatorias'),
    path('convocatorias/<int:pk>/editar/', views.editar_convocatoria, name='editar_convocatoria'),
    # path('convocatorias/<int:convocatoria_id>/editar/', views.editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/<int:convocatoria_id>/eliminar/', eliminar_convocatoria, name='eliminar_convocatoria'),
    path('convocatorias/<int:convocatoria_id>/alineacion/lapa/', views.gestionar_alineacion_lapa, name='gestionar_alineacion_lapa'),
    path('convocatorias/<int:convocatoria_id>/alineacion/snp/', views.gestionar_alineacion_snp, name='gestionar_alineacion_snp'),

    
]
