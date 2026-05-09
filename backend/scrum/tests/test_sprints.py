from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from ..models import Project, Sprint, ProjectMembership

User = get_user_model()

class ApiSprintNoLoginTestCase(TestCase):
    def test_nologin(self):
        response = self.client.get(path=reverse('task-list-create'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(path=reverse('task-detail', args=[1]))
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(path=reverse('task-detail', args=[1]))
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(path=reverse('task-detail', args=[1]))
        self.assertEqual(response.status_code, 403)

class ApiSprintCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
        ]

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER)

    def test_create(self):
        self.client.force_login(self.users[0])

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

        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.users[0])
        
        response = self.client.post(path=reverse('sprint-list-create'))
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path=reverse('sprint-list-create'), data={'name': 'test'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(path=reverse('sprint-list-create'), data={'project': 1})
        self.assertEqual(response.status_code, 400)
    
    def test_no_permission(self):
        self.client.force_login(self.users[1])

        data = {
            'name': 'Test Sprint',
            'project': 1,
            'goal': 'Goal',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'PLANNED'
        }

        response = self.client.post(path=reverse('sprint-list-create'), data=data)

        self.assertEqual(response.status_code, 403)

class ApiSprintListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
        ]

        cls.projects = [
            Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0]),
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.users[0])
        ]

        ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER)

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

    def test_get_list(self):
        self.client.force_login(self.users[0])
        response = self.client.get(path=reverse('sprint-list-create'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.users[0])
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'project': self.projects[0].pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.users[0])
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'ACTIVE'}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.users[0])
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'PLANNED', 'project': self.projects[1].pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.users[0])
        response = self.client.get(path=reverse('sprint-list-create'), query_params={'status': 'COMPLETED'}) # type: ignore
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        self.assertEqual(len(rd), 0)

    def test_get_list_user1(self):
        self.client.force_login(self.users[1])
        response = self.client.get(path=reverse('sprint-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
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