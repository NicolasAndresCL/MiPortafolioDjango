import os
from pathlib import Path
from datetime import timedelta

from typing import Annotated

import dj_database_url
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuración tipada y validada, leída desde el entorno / .env."""

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, '.env'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )

    SECRET_KEY: str = ''
    DEBUG: bool = False
    ALLOWED_HOSTS: Annotated[list[str], NoDecode] = []
    EMBED_REACT: bool = False

    DATABASE_URL: str = ''

    CORS_ALLOWED_ORIGINS: Annotated[list[str], NoDecode] = []

    EMAIL_HOST_USER: str = ''
    EMAIL_HOST_PASSWORD: str = ''
    DEFAULT_FROM_EMAIL: str = ''
    CONTACT_RECIPIENT_EMAIL: str = ''

    # Flags de seguridad HTTPS — se aplican en settings.production (gated por entorno)
    SECURE_SSL_REDIRECT: bool = False
    SECURE_HSTS_SECONDS: int = 0
    SESSION_COOKIE_SECURE: bool = False
    CSRF_COOKIE_SECURE: bool = False

    @field_validator('ALLOWED_HOSTS', 'CORS_ALLOWED_ORIGINS', mode='before')
    @classmethod
    def _split_csv(cls, value):
        # Acepta CSV ("a,b,c") además de JSON, por compatibilidad con el .env existente.
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return value


conf = Settings()

SECRET_KEY = conf.SECRET_KEY
DEBUG = conf.DEBUG
ALLOWED_HOSTS = conf.ALLOWED_HOSTS
EMBED_REACT = conf.EMBED_REACT

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
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'static', 'frontend', 'dist'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portfolio_app.context_processors.vite_assets',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# PostgreSQL si hay DATABASE_URL; si no, SQLite (preserva el deploy en PythonAnywhere).
if conf.DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(conf.DATABASE_URL, conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if EMBED_REACT:
    STATICFILES_DIRS += [
        os.path.join(BASE_DIR, 'static', 'frontend', 'dist'),
        os.path.join(BASE_DIR, 'static', 'frontend', 'dist', 'assets'),
        os.path.join(BASE_DIR, 'static', 'swagger'),
    ]

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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '300/min',
        'login': '10/min',
    },
    'EXCEPTION_HANDLER': 'portfolio_app.exceptions.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Portafolio Backend — Django & DRF API',
    'DESCRIPTION': (
        'Documentación interactiva y profesional de la API REST de mi portafolio personal, '
        'desarrollada con Django y Django REST Framework. '
        'Incluye autenticación JWT, gestión modular de proyectos, habilidades y contacto. '
        'La interfaz Swagger UI ha sido personalizada con drf-spectacular-sidecar, '
        'estilos técnicos en tonos azules y branding propio.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'displayOperationId': True,
    },
}

# Email — credenciales desde variables de entorno
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = conf.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = conf.DEFAULT_FROM_EMAIL or conf.EMAIL_HOST_USER
CONTACT_RECIPIENT_EMAIL = conf.CONTACT_RECIPIENT_EMAIL or conf.EMAIL_HOST_USER
