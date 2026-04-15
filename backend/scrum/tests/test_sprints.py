from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, Sprint

User = get_user_model()

class ApiSprintNoLoginTestCase(TestCase):
    def test_nologin(self):
        response = self.client.get(path=reverse('task-list-create'))
        self.assertEqual(response.status_code, 403)

class ApiSprintCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**userdata)

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.user)

    def setUp(self) -> None:
        self.client.login(username='jtp', password='pass')

    def test_create(self):
        data = {
            'name': 'Test Sprint',
            'project': 1
        }

        response = self.client.post(path=reverse('sprint-list-create'), data=data)

        self.assertEqual(response.status_code, 201)

        sprint = Sprint.objects.get(pk=1)

        self.assertEqual(sprint.project, self.project)
        self.assertEqual(sprint.name, data['name'])
        self.assertIn(sprint, self.project.sprints.all())

        rd = response.json()

        self.assertEqual(rd['name'], data['name'])
    
    def test_missing(self):
        response = self.client.post(path=reverse('sprint-list-create'))
        self.assertEqual(response.status_code, 400)

class ApiSprintListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**userdata)

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.user)
        cls.sprints = [
            Sprint.objects.create(name='Sprint 1', project=cls.project),
            Sprint.objects.create(name='Sprint 2', project=cls.project)
        ]

    def setUp(self) -> None:
        self.client.login(username='jtp', password='pass')

    def test_get_list(self):
        response = self.client.get(path=reverse('sprint-list-create'))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        self.assertTrue((rd[0]['name'] == 'Sprint 1' and rd[1]['name'] == 'Sprint 2') or (rd[1]['name'] == 'Sprint 1' and rd[0]['name'] == 'Sprint 2'))