from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, Skill
import os

class ProjectModelTest(TestCase):
    def setUp(self):
        # Crear un archivo de imagen simulado para la prueba
        self.image_content = b"file_content"
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=self.image_content,
            content_type='image/jpeg'
        )

    def test_project_creation(self):
        """
        Verifica que un proyecto se puede crear correctamente y sus atributos son correctos.
        """
        project = Project.objects.create(
            title="Mi Proyecto de Prueba",
            description="Esta es una descripción de prueba para el proyecto.",
            image=self.test_image,
            github_link="https://github.com/test/project",
            live_link="https://test-project.com",
            technologies="Python, Django, Testing",
            is_featured=True
        )

        self.assertEqual(project.title, "Mi Proyecto de Prueba")
        self.assertEqual(project.description, "Esta es una descripción de prueba para el proyecto.")
        self.assertEqual(project.github_link, "https://github.com/test/project")
        self.assertEqual(project.live_link, "https://test-project.com")
        self.assertEqual(project.technologies, "Python, Django, Testing")
        self.assertTrue(project.is_featured)
        self.assertIsNotNone(project.created_at)
        self.assertTrue('projects/test_image.jpg' in project.image.name)

        # Asegurarse de que el archivo se ha guardado si imagefield lo hace
        # (Esto puede variar según la configuración de MEDIA_ROOT y almacenamiento)
        # self.assertTrue(os.path.exists(project.image.path))


    def test_project_str_representation(self):
        """
        Verifica que el método __str__ de Project devuelve el título.
        """
        project = Project.objects.create(
            title="Otro Proyecto",
            description="Descripción",
            technologies="Tech"
        )
        self.assertEqual(str(project), "Otro Proyecto")

    def test_project_optional_fields(self):
        """
        Verifica que los campos opcionales (blank=True, null=True) funcionan correctamente.
        """
        project = Project.objects.create(
            title="Proyecto Sin Detalles",
            description="Solo una descripción."
            # No se proporcionan image, github_link, live_link, technologies, is_featured (usará defaults)
        )
        self.assertIsNone(project.image.name) # blank=True para ImageField significa que el nombre de archivo es None si no se sube
        self.assertEqual(project.github_link, "")
        self.assertEqual(project.live_link, "")
        self.assertFalse(project.is_featured) # Default es False

    def tearDown(self):
        # Limpiar cualquier archivo creado durante las pruebas (si tu almacenamiento lo requiere)
        # Esto es importante para evitar acumulación de archivos de prueba
        for project in Project.objects.all():
            if project.image:
                if os.path.exists(project.image.path):
                    project.image.delete(save=False) # save=False para no intentar guardar el modelo sin archivo


class SkillModelTest(TestCase):
    def test_skill_creation(self):
        """
        Verifica que una habilidad se puede crear correctamente y sus atributos son correctos.
        """
        skill = Skill.objects.create(
            name="Python",
            level=9,
            category="Backend"
        )
        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.level, 9)
        self.assertEqual(skill.category, "Backend")

    def test_skill_str_representation(self):
        """
        Verifica que el método __str__ de Skill devuelve el nombre.
        """
        skill = Skill.objects.create(
            name="Django",
            level=8
        )
        self.assertEqual(str(skill), "Django")

    def test_skill_default_level(self):
        """
        Verifica que el campo 'level' tiene el valor por defecto correcto.
        """
        skill = Skill.objects.create(
            name="CSS"
        )
        self.assertEqual(skill.level, 5) # Default es 5

    def test_skill_optional_category(self):
        """
        Verifica que el campo 'category' es opcional.
        """
        skill = Skill.objects.create(
            name="JavaScript",
            level=7
        )
        self.assertIsNone(skill.category) # Null=True permite que sea Noneñ