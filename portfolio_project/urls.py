from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from portfolio_app.views import ProjectViewSet, SkillViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import environ
from django.views.generic.base import RedirectView



env = environ.Env()
environ.Env.read_env()

EMBED_REACT = env.bool('EMBED_REACT', default=False)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api/', include('portfolio_app.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Añade STATIC_ROOT

if EMBED_REACT:
    urlpatterns += [
        
        re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
    ]
else:
    urlpatterns += [
        path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    ]