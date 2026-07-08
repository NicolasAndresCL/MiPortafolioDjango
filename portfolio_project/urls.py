from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from portfolio_app.views import (
    ProjectViewSet,
    SkillViewSet,
    ExperienceViewSet,
    ExperienceHighlightViewSet,
    health_check,
)


class CustomSwaggerView(TemplateView):
    template_name = 'swagger/custom_swagger.html'


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'experience', ExperienceViewSet)
router.register(r'experience-highlights', ExperienceHighlightViewSet)

urlpatterns = [
    path('healthz/', health_check, name='healthz'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('portfolio_app.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', CustomSwaggerView.as_view(), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.EMBED_REACT:
    urlpatterns += [
        re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
    ]
else:
    urlpatterns += [
        path('', RedirectView.as_view(url='api/schema/swagger-ui/', permanent=False)),
    ]
