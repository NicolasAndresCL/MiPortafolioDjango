import os
from pathlib import Path
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # ¡Añade DRF!
    'rest_framework.authtoken', # Para autenticación
    'portfolio_app', # ¡Añade tu app!
    'drf_spectacular', # Para documentación de la API
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middleware para manejar CORS
    'django.middleware.common.CommonMiddleware', 
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'), # Django buscará archivos estáticos aquí
#]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración básica de DRF (puedes expandirla más adelante)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Para permitir GET sin token
                                            # Puedes cambiar esto a IsAuthenticated
                                            # si necesitas autenticación para los endpoints de la API.
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Si quieres usar autenticación de token, asegúrate de tener 'rest_framework.authtoken'
    # en INSTALLED_APPS y configurarlo aquí.
    'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    ]
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Tu frontend local (ej. React)
    "http://127.0.0.1:3000",
    "https://nicolasandrescl.github.io", # Tu frontend en producción
]


SPECTACULAR_SETTINGS = {
    'TITLE': 'Portafolio API',
    'DESCRIPTION': 'API para gestionar proyectos y habilidades de mi portafolio personal con Django y DRF. Documentación automatizada con drf-spectacular.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, # Si quieres servir el archivo schema.json directamente
    # 'SWAGGER_UI_SETTINGS': {
    #     'dom_id': '#swagger-ui',
    #     'layout': 'BaseLayout',
    #     'deepLinking': True,
    # },
    # 'REDOC_UI_SETTINGS': {
    #     'nativeScrollbars': True,
    #     'theme': {
    #         'colors': {
    #             'primary': {
    #                 'main': '#61dafb'
    #             }
    #         }
    #     }
    # },
    # ... muchas más opciones, revisa la documentación para personalización avanzada
}

# Configuración de Correo Electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'canolealn@gmail.com' # ¡CAMBIA ESTO por tu correo de Gmail!
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # Genera tu contraseña de aplicaciones en https://myaccount.google.com!
DEFAULT_FROM_EMAIL = 'canolealn@gmail.com' # La dirección que aparecerá como remitente

# Opcional: Desactivar la verificación SSL si tienes problemas (no recomendado para producción)
# EMAIL_USE_SSL = False
# EMAIL_VERIFY_SSL_CERT = False