from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio_app.views import ProjectViewSet, SkillViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


# Crea un router para tus ViewSets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Tus URLs de la API de DRF
    path('', include('portfolio_app.urls')), # ¡Añade esta línea! La raíz apuntará a las URLs de tu app

    # --- URLs para DRF Spectacular ---
    # Ruta para el esquema OpenAPI (YAML/JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Ruta para la interfaz de usuario de Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Ruta para la interfaz de usuario de ReDoc (alternativa a Swagger UI)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # --- Fin URLs para DRF Spectacular ---
]

# Configuración para servir archivos estáticos/media en desarrollo (solo para desarrollo)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)