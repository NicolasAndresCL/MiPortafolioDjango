from .base import *

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# En desarrollo usar la consola en lugar de SMTP real
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
