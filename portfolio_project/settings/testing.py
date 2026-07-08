from .base import *

# Configuración mínima para ejecutar tests sin archivo .env
SECRET_KEY = 'django-insecure-testing-key-not-for-production-use'
DEBUG = True
ALLOWED_HOSTS = ['*']
EMBED_REACT = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST_USER = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'
CONTACT_RECIPIENT_EMAIL = 'test@example.com'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

# Desactivar throttling en tests: el contador por IP se acumularía entre requests
# de la suite y produciría 429 espurios.
REST_FRAMEWORK = {**REST_FRAMEWORK, 'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_THROTTLE_RATES': {}}
