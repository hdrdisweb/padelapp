from django.contrib import admin
from django.urls import path, include
from .views import user_login, dashboard, user_logout, profile
from . import views 
from padelapp.views import crear_partido, gestionar_partido, lista_partidos  



urlpatterns = [
    path("grappelli/", include("grappelli.urls")),  # Grappelli para mejorar el admin
    path("admin/", admin.site.urls),  # Admin de Django
    path("", user_login, name="login"),  # Página principal -> login
    path('registro/', views.register, name='register'),
    path("dashboard/", dashboard, name="dashboard"),  # Dashboard
    path("logout/", user_logout, name="logout"),  # Cerrar sesión
    path("profile/", profile, name="profile"),  # Añadimos la ruta para el perfil

    # Incluir rutas de la app "padelapp"
    path("padel/", include("padelapp.urls")),
    path('partidos/', lista_partidos, name='lista_partidos'),  # 🔹 Listar partidos
    path('partidos/crear/', crear_partido, name='crear_partido'),  # 🔹 Crear un partido
    path('partidos/<int:partido_id>/gestionar/', gestionar_partido, name='gestionar_partido'),  # 🔹 Unirse o salir de un partido


]
