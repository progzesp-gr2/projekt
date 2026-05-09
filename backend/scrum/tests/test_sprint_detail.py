from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from ..models import Project, Sprint, ProjectMembership, Task

User = get_user_model()

class ApiSprintGetTestCase(TestCase):
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

    def test_get(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('sprint-detail', args=[self.sprints[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        
        expect = {
            'id': self.sprints[0].pk,
            'name': 'Sprint 1',
            'project': self.projects[0].pk,
            'goal': 'Goal 1',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'ACTIVE'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
    
    def test_get_not_owner(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('sprint-detail', args=[self.sprints[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.sprints[0].pk,
            'name': 'Sprint 1',
            'project': self.projects[0].pk,
            'goal': 'Goal 1',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'ACTIVE'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)

    def test_get_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('sprint-detail', args=[self.sprints[2].pk]))

        self.assertEqual(response.status_code, 404)
    
    def test_get_missing(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('sprint-detail', args=[999]))

        self.assertEqual(response.status_code, 404)
    
class ApiSprintUpdateTestCase(TestCase):
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

        cls.sprint = Sprint.objects.create(
            name='Sprint 1',
            project=cls.projects[0],
            goal='Goal 1',
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 15),
            status=Sprint.SprintStatus.ACTIVE
        )
    
    def test_update(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('sprint-detail', args=[self.sprint.pk]),
            data={'goal': 'changed'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sprint.objects.get(pk=self.sprint.pk).goal, 'changed')

        rd = response.json()

        expect = {
            'id': self.sprint.pk,
            'name': 'Sprint 1',
            'project': self.projects[0].pk,
            'goal': 'changed',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'ACTIVE'
        }

        for k, v in expect.items():
            self.assertEqual(rd[k], v)
    
    def test_update_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.patch(
            path=reverse('sprint-detail', args=[self.sprint.pk]), 
            data={'status': 'COMPLETED'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
    
    def test_update_empty(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('sprint-detail', args=[self.sprint.pk]), 
            data={},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.sprint.pk,
            'name': 'Sprint 1',
            'project': self.projects[0].pk,
            'goal': 'Goal 1',
            'start_date': '2026-01-01',
            'end_date': '2026-01-15',
            'status': 'ACTIVE'
        }

        for k, v in expect.items():
            self.assertEqual(rd[k], v)

class ApiSprintDeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
        ]

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])

        cls.sprint = Sprint.objects.create(
            name='Sprint 1',
            project=cls.project,
            goal='Goal 1',
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 15),
            status=Sprint.SprintStatus.ACTIVE
        )
        cls.task = Task.objects.create(
            title='Task 1',
            project=cls.project,
            sprint=cls.sprint,
            reporter=cls.users[0],
            assignee=cls.users[0],
            description='desc 1',
            task_type=Task.TaskType.STORY,
            status=Task.TaskStatus.TODO,
            priority=Task.TaskPriority.LOW
        )
    
    def test_delete(self):
        self.client.force_login(self.users[0])

        response = self.client.delete(path=reverse('sprint-detail', args=[self.sprint.pk]))

        self.assertEqual(response.status_code, 204)

        self.assertTrue(Project.objects.contains(self.project))
        self.assertFalse(Sprint.objects.contains(self.sprint))
        self.assertTrue(Task.objects.contains(self.task))
        self.assertIsNone(Task.objects.get(pk=self.task.pk).sprint)

    def test_delete_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.delete(path=reverse('sprint-detail', args=[self.sprint.pk]))

        self.assertEqual(response.status_code, 404)

        self.assertTrue(Project.objects.contains(self.project))
        self.assertTrue(Sprint.objects.contains(self.sprint))
        self.assertTrue(Task.objects.contains(self.task))
        self.assertIsNotNone(Task.objects.get(pk=self.task.pk).sprint)