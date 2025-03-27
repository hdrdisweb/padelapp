from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from padelapp.models import Notification  # Solo importar lo necesario
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.core.mail import EmailMessage
from .forms import ContactForm

def index(request):
    return render(request, 'index.html')

def user_login(request):
    """Vista para el inicio de sesión"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

def user_logout(request):
    """Cerrar sesión y redirigir al login"""
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    """Vista del dashboard donde se muestran las notificaciones"""
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return render(request, 'dashboard.html', {'notifications': notifications})

# vista de registro
User = get_user_model()

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        # Validaciones básicas
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return redirect('register')

        # Crear usuario con el modelo personalizado
        user = User.objects.create_user(
            first_name=name,
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, 'Cuenta creada con éxito. ¡Ahora puedes iniciar sesión!')
        return redirect('login')

    return render(request, 'registro.html')

# vista del perfil
from django.contrib import messages
from django.shortcuts import render, redirect

def profile(request):
    user = request.user

    if request.method == "POST":
        try:
            # Carga los datos básicos
            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.email = request.POST.get("email", "").strip()
            user.dni_nie = request.POST.get("dni_nie", "").strip()
            user.movil = request.POST.get("movil", "").strip()
            user.provincia = request.POST.get("provincia", "").strip()

            # Controlamos errores básicos
            if not user.email:
                messages.error(request, "El correo es obligatorio.")
            elif User.objects.exclude(id=user.id).filter(email=user.email).exists():
                messages.error(request, "Este correo ya está en uso.")
            elif user.dni_nie and User.objects.exclude(id=user.id).filter(dni_nie=user.dni_nie).exists():
                messages.error(request, "Este DNI/NIE ya está registrado.")
            else:
                user.save()
                messages.success(request, "Perfil actualizado correctamente.")
                return redirect("profile")

        except Exception as e:
            messages.error(request, f"Error al actualizar el perfil: {e}")

    return render(request, "profile_content.html")



# vista para qeu no puedan los jugadores crear pull

def crear_pull(request):
    if not request.user.is_staff:
        messages.error(request, "No estás autorizado para crear una pull.")
        return redirect('lista_pulls') 


# pagina de contacto  

def contacto_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = EmailMessage(
                subject=data['subject'],
                body=f"Mensaje de {data['name']} <{data['email']}>\n\n{data['message']}",
                from_email=data['email'],
                to=['tucorreo@dominio.com'],  # reemplazar con tu email real
            )
            try:
                email.send()
                messages.success(request, 'Tu mensaje ha sido enviado correctamente.')
            except:
                messages.error(request, 'Ocurrió un error al enviar el mensaje. Intenta más tarde.')
            return redirect('contacto')
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})