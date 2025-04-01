from django.contrib import admin
from django.urls import path, include
from .views import user_login, dashboard, user_logout, profile
from . import views 
from padelapp.views import crear_partido, gestionar_partido, lista_partidos  
from .views import index
from .views import contacto_view 
from .views import faq_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    
    path("", index, name="index"),  # 👈 Ahora el index es la raíz
    path("login/", user_login, name="login"),  # 👈 Movemos el login a su ruta real
    
    path('registro/', views.register, name='register'),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", user_logout, name="logout"),
    path("profile/", profile, name="profile"),
    
    path("padel/", include("padelapp.urls")),
    path('partidos/', lista_partidos, name='lista_partidos'),
    path('partidos/crear/', crear_partido, name='crear_partido'),
    path('partidos/<int:partido_id>/gestionar/', gestionar_partido, name='gestionar_partido'),
    path('contacto/', contacto_view, name='contacto'),
    path('faq/', faq_view, name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)