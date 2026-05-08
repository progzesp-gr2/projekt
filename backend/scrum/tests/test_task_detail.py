from ..models import Project, Sprint, Task, ProjectMembership
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import date

User = get_user_model()

class ApiTaskGetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com')
        ]
        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER)
        cls.sprint = Sprint.objects.create(
            name='Sprint 1',
            project=cls.project,
            goal='Goal 1',
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 15),
            status=Sprint.SprintStatus.ACTIVE
        )
        cls.tasks = [
            Task.objects.create(
                title='Task 1',
                project=cls.project,
                sprint=cls.sprint,
                reporter=cls.users[0],
                assignee=cls.users[0],
                description='desc 1',
                task_type=Task.TaskType.STORY,
                status=Task.TaskStatus.TODO,
                priority=Task.TaskPriority.LOW
            ),
            Task.objects.create(
                title='Task 2',
                project=cls.project,
                sprint=cls.sprint,
                reporter=cls.users[0],
                assignee=cls.users[1],
                description='desc 2',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_PROGRESS,
                priority=Task.TaskPriority.MEDIUM
            )
        ]
    
    def test_get(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('task-detail', args=[self.tasks[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        
        expect = {
            'id': self.tasks[0].pk,
            'title': 'Task 1',
            'project': self.project.pk,
            'sprint':self.sprint.pk,
            'reporter': self.users[0].pk,
            'assignee': self.users[0].pk,
            'description': 'desc 1',
            'task_type': 'STORY',
            'status': 'TODO',
            'priority': 'LOW'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
    
    def test_get_not_owner(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('task-detail', args=[self.tasks[1].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.tasks[1].pk,
            'title': 'Task 2',
            'project': self.project.pk,
            'sprint':self.sprint.pk,
            'reporter': self.users[0].pk,
            'assignee': self.users[1].pk,
            'description': 'desc 2',
            'task_type': 'BUG',
            'status': 'IN_PROGRESS',
            'priority': 'MEDIUM'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)

    def test_get_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('task-detail', args=[self.tasks[0].pk]))

        self.assertEqual(response.status_code, 404)

class ApiTaskUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com')
        ]
        cls.projects = [
            Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0]),
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.users[0])
        ]
        cls.memberships= [
            ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER),
            ProjectMembership.objects.create(project=cls.projects[1], user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER)
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

        cls.tasks = [
            Task.objects.create(
                title='Task 1',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.users[0],
                assignee=cls.users[1],
                description='desc 1',
                task_type=Task.TaskType.STORY,
                status=Task.TaskStatus.TODO,
                priority=Task.TaskPriority.LOW
            ),
            Task.objects.create(
                title='Task 2',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.users[0],
                assignee=cls.users[1],
                description='desc 2',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_PROGRESS,
                priority=Task.TaskPriority.MEDIUM
            ),
            Task.objects.create(
                title='Task 3',
                project=cls.projects[1],
                sprint=cls.sprints[2],
                reporter=cls.users[0],
                assignee=cls.users[1],
                description='desc 3',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_REVIEW,
                priority=Task.TaskPriority.MEDIUM
            )
        ]
    
    def setUp(self):
        self.client.force_login(self.users[0])
    
    def test_update(self):
        patchdata = {'description': 'changed'}

        response = self.client.patch(path=reverse('task-detail', args=[self.tasks[0].pk]), data=patchdata, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        expect = {
            'id': self.tasks[0].pk,
            'title': 'Task 1',
            'project': self.projects[0].pk,
            'sprint':self.sprints[1].pk,
            'reporter': self.users[0].pk,
            'assignee': self.users[1].pk,
            'description': 'changed',
            'task_type': 'STORY',
            'status': 'TODO',
            'priority': 'LOW'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)

        self.assertEqual(Task.objects.get(pk=self.tasks[0].pk).description, 'changed')
    
    def test_update_no_permission(self):
        self.client.force_login(self.users[1])

        patchdata = {'description': 'changed'}

        response = self.client.patch(path=reverse('task-detail', args=[self.tasks[0].pk]), data=patchdata, content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_update_bad_reporter(self):
        self.client.patch(path=reverse('task-detail', args=[self.tasks[0].pk]), data={'reporter': 2}, content_type='application/json')

        self.assertEqual(Task.objects.get(pk=self.tasks[0].pk).reporter_id, 1) # type: ignore
    
    def test_update_empty(self):
        response = self.client.patch(path=reverse('task-detail', args=[self.tasks[0].pk]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        expect = {
            'id': self.tasks[0].pk,
            'title': 'Task 1',
            'project': self.projects[0].pk,
            'sprint':self.sprints[1].pk,
            'reporter': self.users[0].pk,
            'assignee': self.users[1].pk,
            'description': 'desc 1',
            'task_type': 'STORY',
            'status': 'TODO',
            'priority': 'LOW'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
    
class ApiTaskDeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com')
        ]
        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.PROGRAMMER)
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

        response = self.client.delete(path=reverse('task-detail', args=[self.task.pk]))

        self.assertEqual(response.status_code, 204)

        self.assertFalse(Task.objects.contains(self.task))

    def test_delete_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.delete(path=reverse('task-detail', args=[self.task.pk]))

        self.assertEqual(response.status_code, 404)

        self.assertTrue(Task.objects.contains(self.task))