from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .models import Project, Skill
from .serializers import ProjectSerializer, SkillSerializer
from django.contrib import messages
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    list=extend_schema(
        tags=["Proyectos"],
        summary="Obtener listado de proyectos",
        responses={200: OpenApiResponse(response=ProjectSerializer(many=True))}
    ),
    create=extend_schema(
        tags=["Proyectos"],
        summary="Crear un nuevo proyecto",
        request=ProjectSerializer,
        responses={201: OpenApiResponse(response=ProjectSerializer)}
    ),
    retrieve=extend_schema(
        tags=["Proyectos"],
        summary="Obtener detalle de un proyecto por ID",
        responses={200: OpenApiResponse(response=ProjectSerializer)}
    ),
    update=extend_schema(
        tags=["Proyectos"],
        summary="Actualizar un proyecto completo",
        request=ProjectSerializer,
        responses={200: OpenApiResponse(response=ProjectSerializer)}
    ),
    partial_update=extend_schema(
        tags=["Proyectos"],
        summary="Actualizar parcialmente un proyecto",
        request=ProjectSerializer,
        responses={200: OpenApiResponse(response=ProjectSerializer)}
    ),
    destroy=extend_schema(
        tags=["Proyectos"],
        summary="Eliminar un proyecto",
        responses={204: OpenApiResponse(description="Proyecto eliminado exitosamente")}
    )
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Habilidades"],
        summary="Listar habilidades",
        responses={200: OpenApiResponse(response=SkillSerializer(many=True))}
    ),
    create=extend_schema(
        tags=["Habilidades"],
        summary="Crear habilidad",
        request=SkillSerializer,
        responses={201: SkillSerializer}
    ),
    retrieve=extend_schema(
        tags=["Habilidades"],
        summary="Obtener habilidad",
        responses={200: SkillSerializer}
    ),
    update=extend_schema(
        tags=["Habilidades"],
        summary="Actualizar habilidad",
        request=SkillSerializer,
        responses={200: SkillSerializer}
    ),
    partial_update=extend_schema(
        tags=["Habilidades"],
        summary="Actualizar parcialmente habilidad",
        request=SkillSerializer,
        responses={200: SkillSerializer}
    ),
    destroy=extend_schema(
        tags=["Habilidades"],
        summary="Eliminar habilidad",
        responses={204: None}
    )
)
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('-level')
    serializer_class = SkillSerializer


# --- Vista principal Solo para templates---
def home(request):
    projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:10]
    skills = Skill.objects.all().order_by('-level')

    context = {
        'projects': projects,
        'skills': skills,
        'nombre_portfolio': 'Nicolás Cano Leal',
        'descripcion_corta': 'Desarrollador Backend Python con experiencia en la construcción de APIs robustas y escalables.',
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"DEBUG: Formulario recibido - Nombre: {name}, Email: {email}, Mensaje: {message}")

        if name and email and message:
            subject = f'Mensaje de contacto de tu Portafolio - {name}'
            email_message = f'Nombre: {name}\nEmail: {email}\n\nMensaje:\n{message}'

            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['canolealn@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
                print("DEBUG: Correo enviado con éxito.")
                return redirect('home')
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                context['error_message'] = "Hubo un error al enviar tu mensaje. Inténtalo de nuevo más tarde."
        else:
            print("DEBUG: Faltan campos obligatorios en el formulario.")
            context['error_message'] = "Por favor, completa todos los campos del formulario."

    return render(request, 'portfolio_app/index.html', context)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.mail import send_mail

@csrf_exempt
def contacto_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            subject = f'Mensaje de contacto - {name}'
            full_message = f'Nombre: {name}\nEmail: {email}\n\nMensaje:\n{message}'

            send_mail(
                subject,
                full_message,
                'noreply@miportfolio.com',
                ['canolealn@gmail.com'],  # Tu email
                fail_silently=False,
            )
            return JsonResponse({'status': 'ok', 'message': 'Mensaje enviado correctamente'})
        except Exception as e:
            print('Error:', e)
            return JsonResponse({'status': 'error', 'message': 'Falló el envío'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
