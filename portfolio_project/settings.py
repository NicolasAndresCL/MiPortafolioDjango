import os
from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['nicolasandrescl.pythonanywhere.com','www.nicolasandrescl.pythonanywhere.com']



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




# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

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



STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static','frontend','dist',), 
    os.path.join(BASE_DIR, 'static','frontend','dist','assets'),  

]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', 
                                            
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Si quieres usar autenticación de token, asegúrate de tener 'rest_framework.authtoken'
    # en INSTALLED_APPS y configurarlo aquí.
    'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework.authentication.TokenAuthentication',
    
    ]
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
    'TITLE': 'Portafolio API',
    'DESCRIPTION': 'API para gestionar proyectos y habilidades de mi portafolio personal con Django y DRF. Documentación automatizada con drf-spectacular.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, 
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