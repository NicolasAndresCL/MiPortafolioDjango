import json

from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Project, Skill, Experience, ExperienceHighlight
from .serializers import (
    ProjectSerializer,
    SkillSerializer,
    ExperienceSerializer,
    ExperienceHighlightSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=["Proyectos"],
        summary="Obtener listado de proyectos",
        responses={200: OpenApiResponse(response=ProjectSerializer(many=True))},
    ),
    create=extend_schema(
        tags=["Proyectos"],
        summary="Crear un nuevo proyecto",
        request=ProjectSerializer,
        responses={201: OpenApiResponse(response=ProjectSerializer)},
    ),
    retrieve=extend_schema(
        tags=["Proyectos"],
        summary="Obtener detalle de un proyecto por ID",
        responses={200: OpenApiResponse(response=ProjectSerializer)},
    ),
    update=extend_schema(
        tags=["Proyectos"],
        summary="Actualizar un proyecto completo",
        request=ProjectSerializer,
        responses={200: OpenApiResponse(response=ProjectSerializer)},
    ),
    partial_update=extend_schema(
        tags=["Proyectos"],
        summary="Actualizar parcialmente un proyecto",
        request=ProjectSerializer,
        responses={200: OpenApiResponse(response=ProjectSerializer)},
    ),
    destroy=extend_schema(
        tags=["Proyectos"],
        summary="Eliminar un proyecto",
        responses={204: OpenApiResponse(description="Proyecto eliminado exitosamente")},
    ),
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Habilidades"],
        summary="Listar habilidades",
        responses={200: OpenApiResponse(response=SkillSerializer(many=True))},
    ),
    create=extend_schema(
        tags=["Habilidades"],
        summary="Crear habilidad",
        request=SkillSerializer,
        responses={201: SkillSerializer},
    ),
    retrieve=extend_schema(
        tags=["Habilidades"],
        summary="Obtener habilidad",
        responses={200: SkillSerializer},
    ),
    update=extend_schema(
        tags=["Habilidades"],
        summary="Actualizar habilidad",
        request=SkillSerializer,
        responses={200: SkillSerializer},
    ),
    partial_update=extend_schema(
        tags=["Habilidades"],
        summary="Actualizar parcialmente habilidad",
        request=SkillSerializer,
        responses={200: SkillSerializer},
    ),
    destroy=extend_schema(
        tags=["Habilidades"],
        summary="Eliminar habilidad",
        responses={204: None},
    ),
)
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('-level')
    serializer_class = SkillSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Experiencia"],
        summary="Obtener listado de experiencia laboral",
        responses={200: OpenApiResponse(response=ExperienceSerializer(many=True))},
    ),
    create=extend_schema(
        tags=["Experiencia"],
        summary="Crear una nueva experiencia laboral",
        request=ExperienceSerializer,
        responses={201: OpenApiResponse(response=ExperienceSerializer)},
    ),
    retrieve=extend_schema(
        tags=["Experiencia"],
        summary="Obtener detalle de una experiencia por ID",
        responses={200: OpenApiResponse(response=ExperienceSerializer)},
    ),
    update=extend_schema(
        tags=["Experiencia"],
        summary="Actualizar una experiencia completa",
        request=ExperienceSerializer,
        responses={200: OpenApiResponse(response=ExperienceSerializer)},
    ),
    partial_update=extend_schema(
        tags=["Experiencia"],
        summary="Actualizar parcialmente una experiencia",
        request=ExperienceSerializer,
        responses={200: OpenApiResponse(response=ExperienceSerializer)},
    ),
    destroy=extend_schema(
        tags=["Experiencia"],
        summary="Eliminar una experiencia",
        responses={204: OpenApiResponse(description="Experiencia eliminada exitosamente")},
    ),
)
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().prefetch_related('highlights').order_by('-start_date')
    serializer_class = ExperienceSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Experiencia"],
        summary="Obtener listado de highlights de experiencia",
        responses={200: OpenApiResponse(response=ExperienceHighlightSerializer(many=True))},
    ),
    create=extend_schema(
        tags=["Experiencia"],
        summary="Crear un highlight asociado a una experiencia",
        request=ExperienceHighlightSerializer,
        responses={201: OpenApiResponse(response=ExperienceHighlightSerializer)},
    ),
    retrieve=extend_schema(
        tags=["Experiencia"],
        summary="Obtener detalle de un highlight por ID",
        responses={200: OpenApiResponse(response=ExperienceHighlightSerializer)},
    ),
    update=extend_schema(
        tags=["Experiencia"],
        summary="Actualizar un highlight completo",
        request=ExperienceHighlightSerializer,
        responses={200: OpenApiResponse(response=ExperienceHighlightSerializer)},
    ),
    partial_update=extend_schema(
        tags=["Experiencia"],
        summary="Actualizar parcialmente un highlight",
        request=ExperienceHighlightSerializer,
        responses={200: OpenApiResponse(response=ExperienceHighlightSerializer)},
    ),
    destroy=extend_schema(
        tags=["Experiencia"],
        summary="Eliminar un highlight",
        responses={204: OpenApiResponse(description="Highlight eliminado exitosamente")},
    ),
)
class ExperienceHighlightViewSet(viewsets.ModelViewSet):
    queryset = ExperienceHighlight.objects.all().order_by('order', 'id')
    serializer_class = ExperienceHighlightSerializer


@extend_schema(
    tags=["Contacto"],
    summary="Enviar mensaje de contacto",
    description="Recibe nombre, email y mensaje; envía un correo al propietario del portafolio.",
    request={"application/json": {"name": "string", "email": "string", "message": "string"}},
    responses={
        200: OpenApiResponse(description="Mensaje enviado correctamente"),
        400: OpenApiResponse(description="Campos requeridos faltantes"),
        405: OpenApiResponse(description="Método no permitido"),
        500: OpenApiResponse(description="Error interno al enviar el correo"),
    },
)
@csrf_exempt
@require_http_methods(["POST"])
def contacto_api(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return JsonResponse(
            {'status': 'error', 'message': 'Todos los campos son requeridos: name, email, message'},
            status=400,
        )

    subject = f'Mensaje de contacto — {name}'
    body = f'Nombre: {name}\nEmail: {email}\n\nMensaje:\n{message}'

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_RECIPIENT_EMAIL],
            fail_silently=False,
        )
        return JsonResponse({'status': 'ok', 'message': 'Mensaje enviado correctamente'})
    except Exception as exc:
        return JsonResponse({'status': 'error', 'message': 'Error al enviar el mensaje'}, status=500)


# ─── JWT Auth views con documentación Swagger ──────────────────────────────────

_login_example = OpenApiExample(
    name="Credenciales de acceso",
    value={"username": "jugador_arcade", "password": "1234seguro"},
    request_only=True,
)

_login_response = OpenApiResponse(
    response={"access": "jwt-token", "refresh": "jwt-refresh-token"},
    description="Tokens generados exitosamente",
)


@extend_schema_view(
    post=extend_schema(
        operation_id="login_usuario",
        summary="Autenticación JWT (Login)",
        description="Genera tokens de acceso y renovación JWT para usuarios registrados.",
        request={"application/json": {"username": "string", "password": "string"}},
        tags=["Autenticación"],
        examples=[_login_example],
        responses={200: _login_response, 401: OpenApiResponse(description="Credenciales inválidas")},
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    # Rate limit específico de login: 10/min (scope 'login' en DEFAULT_THROTTLE_RATES).
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'


_refresh_example = OpenApiExample(
    name="Token de renovación",
    value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ..."},
    request_only=True,
)

_refresh_response = OpenApiResponse(
    response={"access": "jwt-new-access-token"},
    description="Nuevo token de acceso generado",
)


@extend_schema_view(
    post=extend_schema(
        operation_id="refrescar_token",
        summary="Renovar token de acceso",
        description="Usa un refresh token válido para generar uno nuevo sin volver a iniciar sesión.",
        request={"application/json": {"refresh": "string"}},
        tags=["Autenticación"],
        examples=[_refresh_example],
        responses={200: _refresh_response, 401: OpenApiResponse(description="Token expirado o inválido")},
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


# ─── Healthcheck (readiness) ───────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Readiness probe: verifica la conexión a la base de datos.

    200 {"status": "ok"} si la DB responde; 503 en caso contrario.
    Sin autenticación — pensado para orquestadores (Docker/K8s) y monitoreo.
    """
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({'status': 'error', 'database': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok'})
