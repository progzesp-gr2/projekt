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
            'project': 1,
            'goal': 'Goal',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'PLANNED'
        }

        response = self.client.post(path=reverse('sprint-list-create'), data=data)

        self.assertEqual(response.status_code, 201)

        rd = response.json()

        sprint = Sprint.objects.get(pk=rd['id'])

        self.assertEqual(sprint.project, self.project)
        self.assertEqual(sprint.name, data['name'])
        self.assertEqual(sprint.start_date, date(2026, 1, 1))
        self.assertEqual(sprint.end_date, date(2026, 1, 15))
        self.assertEqual(sprint.status, Sprint.SprintStatus.PLANNED)
        self.assertIn(sprint, self.project.sprints.all()) # type: ignore

        self.assertTrue(all(rd[k] == data[k] for k in data.keys()))
    
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

        cls.projects = [
            Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.user),
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.user)
        ]
        cls.sprints = [
            Sprint.objects.create(
                name='Sprint 1',
                project=cls.projects[0],
                goal='Goal 1',
                start_date=date(2026, 1, 1),
                end_date=date(2026, 1, 15),
                status=Sprint.SprintStatus.ACTIVE
            ),
            Sprint.objects.create(
                name='Sprint 2',
                project=cls.projects[0],
                goal='Goal 2',
                start_date=date(2026, 1, 15),
                end_date=date(2026, 1, 30),
                status=Sprint.SprintStatus.PLANNED
            ),
            Sprint.objects.create(
                name='Sprint 3',
                project=cls.projects[1],
                goal='Goal 3',
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
            match sprint['name']:
                case 'Sprint 1':
                    self.assertEqual(sprint['project'], self.projects[0].pk)
                    self.assertEqual(sprint['goal'], 'Goal 1')
                    self.assertEqual(sprint['start_date'], '2026-01-01')
                    self.assertEqual(sprint['end_date'], '2026-01-15')
                    self.assertEqual(sprint['status'], 'ACTIVE')
                case 'Sprint 2':
                    self.assertEqual(sprint['project'], self.projects[0].pk)
                    self.assertEqual(sprint['goal'], 'Goal 2')
                    self.assertEqual(sprint['start_date'], '2026-01-15')
                    self.assertEqual(sprint['end_date'], '2026-01-30')
                    self.assertEqual(sprint['status'], 'PLANNED')
                case 'Sprint 3':
                    self.assertEqual(sprint['project'], self.projects[1].pk)
                    self.assertEqual(sprint['goal'], 'Goal 3')
                    self.assertEqual(sprint['start_date'], '2026-01-15')
                    self.assertEqual(sprint['end_date'], '2026-01-30')
                    self.assertEqual(sprint['status'], 'PLANNED')
                case _:
                    self.fail()
    
    def test_get_list_project1(self):
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'project': self.projects[0].pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        for sprint in rd:
            match sprint['name']:
                case 'Sprint 1':
                    self.assertEqual(sprint['project'], self.projects[0].pk)
                    self.assertEqual(sprint['goal'], 'Goal 1')
                    self.assertEqual(sprint['start_date'], '2026-01-01')
                    self.assertEqual(sprint['end_date'], '2026-01-15')
                    self.assertEqual(sprint['status'], 'ACTIVE')
                case 'Sprint 2':
                    self.assertEqual(sprint['project'], self.projects[0].pk)
                    self.assertEqual(sprint['goal'], 'Goal 2')
                    self.assertEqual(sprint['start_date'], '2026-01-15')
                    self.assertEqual(sprint['end_date'], '2026-01-30')
                    self.assertEqual(sprint['status'], 'PLANNED')
                case _:
                    self.fail()
    
    def test_get_list_active(self):
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'ACTIVE'}) # type: ignore

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        for sprint in rd:
            match sprint['name']:
                case 'Sprint 1':
                    self.assertEqual(sprint['project'], self.projects[0].pk)
                    self.assertEqual(sprint['goal'], 'Goal 1')
                    self.assertEqual(sprint['start_date'], '2026-01-01')
                    self.assertEqual(sprint['end_date'], '2026-01-15')
                    self.assertEqual(sprint['status'], 'ACTIVE')
                case _:
                    self.fail()
    
    def test_get_list_planned_project2(self):
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'PLANNED', 'project': self.projects[1].pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        for sprint in rd:
            match sprint['name']:
                case 'Sprint 3':
                    self.assertEqual(sprint['project'], self.projects[1].pk)
                    self.assertEqual(sprint['goal'], 'Goal 3')
                    self.assertEqual(sprint['start_date'], '2026-01-15')
                    self.assertEqual(sprint['end_date'], '2026-01-30')
                    self.assertEqual(sprint['status'], 'PLANNED')
                case _:
                    self.fail()

    def test_get_list_empty(self):
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'COMPLETED'}) # type: ignore
        self.assertEqual(response.status_code, 200)

        rd = response.json()
        self.assertEqual(len(rd), 0)
