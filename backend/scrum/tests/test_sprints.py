from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
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
        self.assertTrue(self.client.login(username='jtp', password='pass'))

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
        self.assertIn(sprint, self.project.sprints.all()) # type: ignore

        rd = response.json()

        self.assertEqual(rd['name'], data['name'])
    
    def test_missing(self):
        response = self.client.post(path=reverse('sprint-list-create'))
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path=reverse('sprint-list-create'), data={'name': 'test'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path=reverse('sprint-list-create'), data={'project': 1})
        self.assertEqual(response.status_code, 400)

class ApiSprintListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**userdata)

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.user)
        cls.sprints = [
            Sprint.objects.create(
                name='Sprint 1',
                project=cls.project,
                goal='Goal 1',
                start_date=date(2026, 1, 1),
                end_date=date(2026, 1, 15),
                status=Sprint.SprintStatus.ACTIVE
            ),
            Sprint.objects.create(
                name='Sprint 2',
                project=cls.project,
                goal='Goal 2',
                start_date=date(2026, 1, 15),
                end_date=date(2026, 1, 30),
                status=Sprint.SprintStatus.PLANNED
            )
        ]

    def setUp(self) -> None:
        self.client.login(username='jtp', password='pass')

    def test_get_list(self):
        response = self.client.get(path=reverse('sprint-list-create'))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        for sprint in rd:
            self.assertEqual(sprint['project'], 1)
            match sprint['name']:
                case 'Sprint 1':
                    self.assertEqual(sprint['goal'], 'Goal 1')
                    self.assertEqual(sprint['start_date'], '2026-01-01')
                    self.assertEqual(sprint['end_date'], '2026-01-15')
                    self.assertEqual(sprint['status'], 'ACTIVE')
                case 'Sprint 2':
                    self.assertEqual(sprint['goal'], 'Goal 2')
                    self.assertEqual(sprint['start_date'], '2026-01-15')
                    self.assertEqual(sprint['end_date'], '2026-01-30')
                    self.assertEqual(sprint['status'], 'PLANNED')
                case _:
                    self.fail()
