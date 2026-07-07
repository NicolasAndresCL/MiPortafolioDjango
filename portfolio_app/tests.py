import json
import os
from datetime import date

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Skill, Experience, ExperienceHighlight


# ─── Model Tests ──────────────────────────────────────────────────────────────

class ProjectModelTest(TestCase):
    def setUp(self):
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg',
        )

    def test_project_creation(self):
        project = Project.objects.create(
            title='Mi Proyecto de Prueba',
            description='Descripción de prueba.',
            image=self.test_image,
            github_link='https://github.com/test/project',
            live_link='https://test-project.com',
            technologies='Python, Django, Testing',
            is_featured=True,
        )
        self.assertEqual(project.title, 'Mi Proyecto de Prueba')
        self.assertEqual(project.github_link, 'https://github.com/test/project')
        self.assertTrue(project.is_featured)
        self.assertIsNotNone(project.created_at)
        self.assertIn('projects/test_image', project.image.name)

    def test_project_str_representation(self):
        project = Project.objects.create(title='Otro Proyecto', description='Desc', technologies='Tech')
        self.assertEqual(str(project), 'Otro Proyecto')

    def test_project_optional_fields(self):
        project = Project.objects.create(title='Sin Detalles', description='Solo desc.')
        self.assertIsNone(project.image.name)
        self.assertEqual(project.github_link, '')
        self.assertEqual(project.live_link, '')
        self.assertFalse(project.is_featured)

    def tearDown(self):
        for project in Project.objects.all():
            if project.image and project.image.name:
                try:
                    if os.path.exists(project.image.path):
                        project.image.delete(save=False)
                except Exception:
                    pass


class SkillModelTest(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(name='Python', level=9, category='Backend')
        self.assertEqual(skill.name, 'Python')
        self.assertEqual(skill.level, 9)
        self.assertEqual(skill.category, 'Backend')

    def test_skill_str_representation(self):
        skill = Skill.objects.create(name='Django', level=8)
        self.assertEqual(str(skill), 'Django')

    def test_skill_default_level(self):
        skill = Skill.objects.create(name='CSS')
        self.assertEqual(skill.level, 5)

    def test_skill_optional_category(self):
        skill = Skill.objects.create(name='JavaScript', level=7)
        self.assertIsNone(skill.category)


class ExperienceModelTest(TestCase):
    def test_experience_creation_is_current(self):
        experience = Experience.objects.create(
            company='PedidosYa',
            role='Live Performance Agent',
            location='Rancagua, Chile',
            start_date=date(2025, 8, 1),
            summary='Automatización de operaciones LiveOps/BizOps.',
            technologies='Python, Django, Docker',
        )
        self.assertEqual(experience.company, 'PedidosYa')
        self.assertIsNone(experience.end_date)
        self.assertTrue(experience.is_current)

    def test_experience_is_current_false_when_end_date_set(self):
        experience = Experience.objects.create(
            company='Empresa Anterior',
            role='Técnico',
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            summary='Rol finalizado.',
        )
        self.assertFalse(experience.is_current)

    def test_experience_str_representation(self):
        experience = Experience.objects.create(
            company='PedidosYa',
            role='Live Performance Agent',
            start_date=date(2025, 8, 1),
            summary='Desc',
        )
        self.assertEqual(str(experience), 'Live Performance Agent @ PedidosYa')

    def test_experience_ordering_by_start_date_desc(self):
        Experience.objects.create(company='A', role='R', start_date=date(2020, 1, 1), summary='D')
        reciente = Experience.objects.create(company='B', role='R', start_date=date(2025, 1, 1), summary='D')
        self.assertEqual(Experience.objects.first(), reciente)


class ExperienceHighlightModelTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            company='PedidosYa',
            role='Live Performance Agent',
            start_date=date(2025, 8, 1),
            summary='Desc',
        )

    def test_highlight_creation_and_relation(self):
        highlight = ExperienceHighlight.objects.create(
            experience=self.experience,
            text='Automatización del bot interno "Jaime".',
            order=1,
        )
        self.assertEqual(self.experience.highlights.count(), 1)
        self.assertEqual(highlight.experience, self.experience)

    def test_highlight_ordering(self):
        ExperienceHighlight.objects.create(experience=self.experience, text='Segundo', order=2)
        ExperienceHighlight.objects.create(experience=self.experience, text='Primero', order=1)
        textos = [h.text for h in self.experience.highlights.all()]
        self.assertEqual(textos, ['Primero', 'Segundo'])

    def test_highlight_str_representation(self):
        highlight = ExperienceHighlight.objects.create(experience=self.experience, text='Texto corto', order=1)
        self.assertEqual(str(highlight), 'Texto corto')


# ─── API Tests: Projects ──────────────────────────────────────────────────────

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='API Test Project',
            description='Proyecto para tests de API.',
            technologies='Python, DRF',
            is_featured=True,
        )

    def test_list_projects(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_project(self):
        url = reverse('project-detail', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Project')

    def test_list_projects_returns_json(self):
        url = reverse('project-list')
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_create_project_unauthenticated_is_forbidden(self):
        url = reverse('project-list')
        data = {'title': 'Nuevo', 'description': 'Desc', 'technologies': 'Python'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_ordering_by_created_at_desc(self):
        Project.objects.create(title='Primero', description='D', technologies='T')
        Project.objects.create(title='Segundo', description='D', technologies='T')
        url = reverse('project-list')
        response = self.client.get(url)
        titles = [p['title'] for p in response.data]
        self.assertEqual(titles[0], 'Segundo')


# ─── API Tests: Skills ────────────────────────────────────────────────────────

class SkillAPITest(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name='Python', level=9, category='Backend')

    def test_list_skills(self):
        url = reverse('skill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_skill(self):
        url = reverse('skill-detail', args=[self.skill.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python')

    def test_skills_ordered_by_level_desc(self):
        Skill.objects.create(name='HTML', level=3)
        Skill.objects.create(name='Django', level=10)
        url = reverse('skill-list')
        response = self.client.get(url)
        levels = [s['level'] for s in response.data]
        self.assertEqual(levels, sorted(levels, reverse=True))

    def test_create_skill_unauthenticated_is_forbidden(self):
        url = reverse('skill-list')
        response = self.client.post(url, {'name': 'Rust', 'level': 4}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── API Tests: Experience ─────────────────────────────────────────────────────

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            company='PedidosYa',
            role='Live Performance Agent',
            location='Rancagua, Chile',
            start_date=date(2025, 8, 1),
            summary='Automatización de operaciones LiveOps/BizOps.',
            technologies='Python, Django, Docker',
        )
        ExperienceHighlight.objects.create(experience=self.experience, text='Highlight 1', order=1)

    def test_list_experience(self):
        url = reverse('experience-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_experience_includes_highlights(self):
        url = reverse('experience-detail', args=[self.experience.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['highlights']), 1)
        self.assertEqual(response.data['highlights'][0]['text'], 'Highlight 1')

    def test_experience_is_current_field_in_response(self):
        url = reverse('experience-detail', args=[self.experience.pk])
        response = self.client.get(url)
        self.assertTrue(response.data['is_current'])

    def test_create_experience_unauthenticated_is_forbidden(self):
        url = reverse('experience-list')
        data = {'company': 'Nueva', 'role': 'Rol', 'start_date': '2024-01-01', 'summary': 'Desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_experience_ordering_by_start_date_desc(self):
        Experience.objects.create(
            company='Empresa Antigua', role='Rol', start_date=date(2019, 1, 1), summary='Desc',
        )
        url = reverse('experience-list')
        response = self.client.get(url)
        companies = [e['company'] for e in response.data]
        self.assertEqual(companies[0], 'PedidosYa')


# ─── API Tests: ExperienceHighlight ────────────────────────────────────────────

class ExperienceHighlightAPITest(APITestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            company='PedidosYa',
            role='Live Performance Agent',
            start_date=date(2025, 8, 1),
            summary='Desc',
        )
        self.highlight = ExperienceHighlight.objects.create(
            experience=self.experience, text='Highlight existente', order=1,
        )

    def test_list_highlights(self):
        url = reverse('experiencehighlight-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_highlight(self):
        url = reverse('experiencehighlight-detail', args=[self.highlight.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Highlight existente')

    def test_create_highlight_unauthenticated_is_forbidden(self):
        url = reverse('experiencehighlight-list')
        data = {'experience': self.experience.pk, 'text': 'Nuevo highlight', 'order': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_highlights_ordered_by_order(self):
        ExperienceHighlight.objects.create(experience=self.experience, text='Tercero', order=3)
        ExperienceHighlight.objects.create(experience=self.experience, text='Segundo', order=2)
        url = reverse('experiencehighlight-list')
        response = self.client.get(url)
        orders = [h['order'] for h in response.data]
        self.assertEqual(orders, sorted(orders))


# ─── API Tests: Contact ───────────────────────────────────────────────────────

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CONTACT_RECIPIENT_EMAIL='test@example.com',
    DEFAULT_FROM_EMAIL='noreply@test.com',
)
class ContactAPITest(TestCase):
    def _url(self):
        return reverse('contacto_api')

    def _valid_payload(self):
        return {'name': 'Juan Pérez', 'email': 'juan@example.com', 'message': 'Hola, quiero colaborar.'}

    def test_contact_success(self):
        response = self.client.post(
            self._url(),
            data=json.dumps(self._valid_payload()),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'], 'ok')

    def test_contact_sends_email(self):
        self.client.post(
            self._url(),
            data=json.dumps(self._valid_payload()),
            content_type='application/json',
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertIn('Juan Pérez', sent.subject)
        self.assertIn('juan@example.com', sent.body)
        self.assertIn('Hola, quiero colaborar.', sent.body)

    def test_contact_missing_name(self):
        payload = {'email': 'juan@example.com', 'message': 'Mensaje'}
        response = self.client.post(
            self._url(),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], 'error')

    def test_contact_missing_email(self):
        payload = {'name': 'Juan', 'message': 'Mensaje'}
        response = self.client.post(
            self._url(),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_missing_message(self):
        payload = {'name': 'Juan', 'email': 'juan@example.com'}
        response = self.client.post(
            self._url(),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_empty_fields(self):
        payload = {'name': '', 'email': '', 'message': ''}
        response = self.client.post(
            self._url(),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_invalid_json(self):
        response = self.client.post(
            self._url(),
            data='not-json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contact_only_accepts_post(self):
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
