from .base import *

DEBUG = False

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'https://nicolasandrescl.github.io',
])

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# SMTP real (heredado de base.py con variables de entorno)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
