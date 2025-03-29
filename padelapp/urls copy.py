from django.urls import path
from .views import inscribir_a_partido, inscribir_a_pull
from . import views
from .views import crear_partido, gestionar_partido, lista_partidos
from .views import get_notifications, mark_notifications_as_read, lista_notificaciones, salir_pull





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
    path('notifications/', get_notifications, name='get_notifications'),
    path('notifications/read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path("notificaciones/", lista_notificaciones, name="lista_notificaciones"),
    path('pull/<int:id>/salir/', salir_pull, name='salir_pull'),


    

    
    
]
