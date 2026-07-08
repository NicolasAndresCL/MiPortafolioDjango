from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False

CORS_ALLOWED_ORIGINS = conf.CORS_ALLOWED_ORIGINS or [
    'https://nicolasandrescl.github.io',
]

# Validación de SECRET_KEY débil en producción
if not SECRET_KEY or SECRET_KEY.startswith('django-insecure') or len(SECRET_KEY) < 32:
    raise ImproperlyConfigured(
        'SECRET_KEY ausente o insegura en producción. Define una clave fuerte (>=32 chars) en el entorno.'
    )

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS endurecido — gated por entorno para no romper PythonAnywhere hasta activarlo por variable.
SECURE_SSL_REDIRECT = conf.SECURE_SSL_REDIRECT
SECURE_HSTS_SECONDS = conf.SECURE_HSTS_SECONDS
SECURE_HSTS_INCLUDE_SUBDOMAINS = conf.SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = conf.SECURE_HSTS_SECONDS > 0
SESSION_COOKIE_SECURE = conf.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = conf.CSRF_COOKIE_SECURE
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# WhiteNoise: estáticos comprimidos (sin manifest, para no arriesgar el deploy actual).
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

# SMTP real (heredado de base.py con variables de entorno)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
