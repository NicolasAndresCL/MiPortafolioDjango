import os
from pathlib import Path
from decouple import config
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'portfolio_app', 
    'drf_spectacular',
    'drf_spectacular_sidecar', 
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'static','frontend','dist',),
            os.path.join(BASE_DIR,'templates',),  

        ],
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

WSGI_APPLICATION = 'portfolio_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

EMBED_REACT = env.bool('EMBED_REACT', default=False)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if EMBED_REACT:
    STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'static', 'frontend', 'dist'))
    STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'static', 'frontend', 'dist', 'assets'))
    STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'static', 'swagger'))


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
    "http://localhost:8000",  
    "http://127.0.0.1:8000",   
    "https://nicolasandrescl.github.io", 
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Portafolio Backend — Django & DRF API ',
    'DESCRIPTION': (
    "Documentación interactiva y profesional de la API REST de mi portafolio personal, desarrollada con Django, Django REST Framework. "
    "Incluye autenticación JWT, gestión modular de proyectos, habilidades y contacto, con trazabilidad completa. "
    "La interfaz Swagger UI ha sido personalizada mediante drf-spectacular y drf-spectacular-sidecar, con override visual desacoplado, estilos técnicos en tonos azules y branding propio. "
    "Se integran assets locales, favicon, logo y layout extendido para mejorar la experiencia de navegación y presentación multiplataforma. "
    "Esta API está diseñada para ser reproducible, escalable y lista para entrevistas técnicas internacionales, con enfoque en claridad, seguridad y presentación visual."
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'displayOperationId': True,
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'canolealn@gmail.com' # ¡CAMBIA ESTO por tu correo de Gmail!
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # Genera tu contraseña de aplicaciones en https://myaccount.google.com!
DEFAULT_FROM_EMAIL = 'canolealn@gmail.com' # La dirección que aparecerá como remitente