import os
from pathlib import Path

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"

# Definir STATIC_ROOT para que Django pueda recopilar archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Configuración para servir archivos estáticos correctamente en producción con Render
if os.getenv('RENDER'):
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATICFILES_DIRS = []  # En producción, los archivos estáticos se sirven desde STATIC_ROOT
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "core", "static")]  # En local, usamos la carpeta de estáticos

# Aplicaciones instaladas
INSTALLED_APPS = [
    "grappelli",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'padelapp',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de rutas
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'padelapp', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'padelapp.wsgi.application'

# Configuración de la base de datos
# 🔹 FORZAMOS el uso de SQLite SIEMPRE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "/static/"

# Configuración diferente para local y producción
if os.getenv('RENDER'):
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATICFILES_DIRS = []  # Render solo usa STATIC_ROOT
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "core", "static")]

# Configuración de la clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'padelapp.User'

# Definir los hosts permitidos
ALLOWED_HOSTS = ["padelapp-jpei.onrender.com", "localhost", "127.0.0.1"]
