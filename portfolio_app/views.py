from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .models import Project, Skill
from .serializers import ProjectSerializer, SkillSerializer
from django.contrib import messages


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Opcional, si quieres restringir la edición, en mi caso lo hice desde settings.py

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('-level') # Ordenar por nivel de habilidad
    serializer_class = SkillSerializer

# --- Nueva Vista para la Página Principal Esto se mostrara en index ---
def home(request):
    # Aquí puedes obtener datos de la base de datos si quieres pasarlos a la plantilla
    projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:10] # Obtener 10 proyectos destacados
    skills = Skill.objects.all().order_by('-level')

    context = {
        'projects': projects,
        'skills': skills,
        'nombre_portfolio': 'Nicolás Cano Leal', # Ejemplo de datos
        'descripcion_corta': 'Desarrollador Backend Python con experiencia en la construcción de APIs robustas y escalables.',
    }

    # Lógica para manejar el envío del formulario de contacto
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"DEBUG: Formulario recibido - Nombre: {name}, Email: {email}, Mensaje: {message}") # Para depuración

        if name and email and message: # Verifica que los campos no estén vacíos
            subject = f'Mensaje de contacto de tu Portafolio - {name}'
            email_message = f'Nombre: {name}\n' \
                            f'Email: {email}\n\n' \
                            f'Mensaje:\n{message}'
            
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['canolealn@gmail.com'], # ¡CAMBIA ESTO por tu correo personal!
                    fail_silently=False,
                )
                messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
                print("DEBUG: Correo enviado con éxito.") # Para depuración
                return redirect('home') # Redirige a la página principal por su nombre de URL (cambiado de 'index' a 'home')
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                context['error_message'] = "Hubo un error al enviar tu mensaje. Inténtalo de nuevo más tarde."
        else:
            print("DEBUG: Faltan campos obligatorios en el formulario.")
            context['error_message'] = "Por favor, completa todos los campos del formulario."

    return render(request, 'portfolio_app/index.html', context)

    