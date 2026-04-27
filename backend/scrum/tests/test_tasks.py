from ..models import Project, Sprint, Task
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse
from datetime import date

User = get_user_model()

class ApiTaskNoLoginTestCase(TestCase):
    def test_nologin(self):
        response = self.client.get(path=reverse('task-list-create'))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(path=reverse('task-list-create'))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(path=reverse('task-update', args=[1]))
        self.assertEqual(response.status_code, 403)


class ApiTaskCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**userdata)
        
        projectdata = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case',
            'owner': cls.user
        }

        cls.project = Project.objects.create(**projectdata)
    
    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create(self):
        taskdata = {
            'title': 'Test Task',
            'project': 1
        }

        response = self.client.post(path=reverse('task-list-create'), data=taskdata)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        taskdata['reporter'] = get_user(self.client).pk

        for key, value in taskdata.items():
            self.assertEqual(rd[key], value)

        task = Task.objects.get(pk=rd['id'])

        taskdata['reporter_id'] = taskdata['reporter']
        del taskdata['reporter']
        taskdata['project_id'] = taskdata['project']
        del taskdata['project']

        for key, value in taskdata.items():
            self.assertEqual(task.__dict__[key], value)

    def test_create_with_reporter(self):
        taskdata = {
            'title': 'Test Task',
            'project': 1,
            'reporter': 1
        }

        response = self.client.post(path=reverse('task-list-create'), data=taskdata)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        taskdata['reporter'] = get_user(self.client).pk

        for key, value in taskdata.items():
            self.assertEqual(rd[key], value)

        task = Task.objects.get(pk=rd['id'])

        taskdata['reporter_id'] = taskdata['reporter']
        del taskdata['reporter']
        taskdata['project_id'] = taskdata['project']
        del taskdata['project']

        for key, value in taskdata.items():
            self.assertEqual(task.__dict__[key], value)
    
    def test_missing(self):
        response = self.client.post(path=reverse('task-list-create'))
        self.assertEqual(response.status_code, 400)

    def test_create_with_different_reporter(self):
        taskdata = {
            'title': 'Test Task',
            'project': 1,
            'reporter': 2
        }

        response = self.client.post(path=reverse('task-list-create'), data=taskdata)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        task = Task.objects.get(pk=rd['id'])

        self.assertEqual(rd['reporter'], 1)
        self.assertEqual(task.reporter, self.user)

class ApiTaskListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com')
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

        cls.tasks = [
            Task.objects.create(
                title='Task 1',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 1',
                task_type=Task.TaskType.STORY,
                status=Task.TaskStatus.TODO,
                priority=Task.TaskPriority.LOW
            ),
            Task.objects.create(
                title='Task 2',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 2',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_PROGRESS,
                priority=Task.TaskPriority.MEDIUM
            ),
            Task.objects.create(
                title='Task 3',
                project=cls.projects[1],
                sprint=cls.sprints[2],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 3',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_REVIEW,
                priority=Task.TaskPriority.MEDIUM
            )
        ]
    
    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_list(self):
        response = self.client.get(path=reverse('task-list-create'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        for task in rd:
            self.assertEqual(task['reporter'], self.user.pk)
            self.assertEqual(task['assignee'], self.user.pk)
            match task['title']:
                case 'Task 1':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 1')
                    self.assertEqual(task['task_type'], 'STORY')
                    self.assertEqual(task['status'], 'TODO')
                    self.assertEqual(task['priority'], 'LOW')
                case 'Task 2':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 2')
                    self.assertEqual(task['task_type'], 'BUG')
                    self.assertEqual(task['status'], 'IN_PROGRESS')
                    self.assertEqual(task['priority'], 'MEDIUM')
                case 'Task 3':
                    self.assertEqual(task['project'], self.projects[1].pk)
                    self.assertEqual(task['sprint'], self.sprints[2].pk)
                    self.assertEqual(task['description'], 'desc 3')
                    self.assertEqual(task['task_type'], 'BUG')
                    self.assertEqual(task['status'], 'IN_REVIEW')
                    self.assertEqual(task['priority'], 'MEDIUM')
                case _:
                    self.fail()

    def test_get_list_sprint_assignee(self):
        response = self.client.get(path=reverse('task-list-create'), query_params={'sprint': self.sprints[1].pk, 'assignee': self.user.pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        for task in rd:
            self.assertEqual(task['reporter'], self.user.pk)
            self.assertEqual(task['assignee'], self.user.pk)
            match task['title']:
                case 'Task 1':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 1')
                    self.assertEqual(task['task_type'], 'STORY')
                    self.assertEqual(task['status'], 'TODO')
                    self.assertEqual(task['priority'], 'LOW')
                case 'Task 2':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 2')
                    self.assertEqual(task['task_type'], 'BUG')
                    self.assertEqual(task['status'], 'IN_PROGRESS')
                    self.assertEqual(task['priority'], 'MEDIUM')
                case _:
                    self.fail()
    
    def test_get_list_project1(self):
        response = self.client.get(path=reverse('task-list-create'), query_params={'project': self.projects[0].pk}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        for task in rd:
            self.assertEqual(task['reporter'], self.user.pk)
            self.assertEqual(task['assignee'], self.user.pk)
            match task['title']:
                case 'Task 1':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 1')
                    self.assertEqual(task['task_type'], 'STORY')
                    self.assertEqual(task['status'], 'TODO')
                    self.assertEqual(task['priority'], 'LOW')
                case 'Task 2':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 2')
                    self.assertEqual(task['task_type'], 'BUG')
                    self.assertEqual(task['status'], 'IN_PROGRESS')
                    self.assertEqual(task['priority'], 'MEDIUM')
                case _:
                    self.fail()

    def test_get_list_in_progress(self):
        response = self.client.get(path=reverse('task-list-create'), query_params={'status': 'IN_PROGRESS'}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        for task in rd:
            self.assertEqual(task['reporter'], self.user.pk)
            self.assertEqual(task['assignee'], self.user.pk)
            match task['title']:
                case 'Task 2':
                    self.assertEqual(task['project'], self.projects[0].pk)
                    self.assertEqual(task['sprint'], self.sprints[1].pk)
                    self.assertEqual(task['description'], 'desc 2')
                    self.assertEqual(task['task_type'], 'BUG')
                    self.assertEqual(task['status'], 'IN_PROGRESS')
                    self.assertEqual(task['priority'], 'MEDIUM')
                case _:
                    self.fail()
    
    def task_get_list_empty(self):
        response = self.client.get(path=reverse('task-list-create'), query_params={'status': 'BACKLOG'}) # type: ignore

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        self.assertEqual(len(rd), 0)

class ApiTaskUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com')
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

        cls.tasks = [
            Task.objects.create(
                title='Task 1',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 1',
                task_type=Task.TaskType.STORY,
                status=Task.TaskStatus.TODO,
                priority=Task.TaskPriority.LOW
            ),
            Task.objects.create(
                title='Task 2',
                project=cls.projects[0],
                sprint=cls.sprints[1],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 2',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_PROGRESS,
                priority=Task.TaskPriority.MEDIUM
            ),
            Task.objects.create(
                title='Task 3',
                project=cls.projects[1],
                sprint=cls.sprints[2],
                reporter=cls.user,
                assignee=cls.user,
                description='desc 3',
                task_type=Task.TaskType.BUG,
                status=Task.TaskStatus.IN_REVIEW,
                priority=Task.TaskPriority.MEDIUM
            )
        ]
    
    def setUp(self):
        self.client.force_login(self.user)
    
    def test_update(self):
        patchdata = {'description': 'changed'}

        response = self.client.patch(path=reverse('task-update', args=[self.tasks[0].pk]), data=patchdata, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        expect = {
            'id': self.tasks[0].pk,
            'title': 'Task 1',
            'project': self.projects[0].pk,
            'sprint':self.sprints[1].pk,
            'reporter': self.user.pk,
            'assignee': self.user.pk,
            'description': 'changed',
            'task_type': 'STORY',
            'status': 'TODO',
            'priority': 'LOW'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)

        self.assertEqual(Task.objects.get(pk=self.tasks[0].pk).description, 'changed')

    def test_update_bad(self):
        self.client.patch(path=reverse('task-update', args=[self.tasks[0].pk]), data={'reporter': 2}, content_type='application/json')

        self.assertEqual(Task.objects.get(pk=self.tasks[0].pk).reporter_id, 1) # type: ignore
    
    def test_update_empty(self):
        response = self.client.patch(path=reverse('task-update', args=[self.tasks[0].pk]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        expect = {
            'id': self.tasks[0].pk,
            'title': 'Task 1',
            'project': self.projects[0].pk,
            'sprint':self.sprints[1].pk,
            'reporter': self.user.pk,
            'assignee': self.user.pk,
            'description': 'desc 1',
            'task_type': 'STORY',
            'status': 'TODO',
            'priority': 'LOW'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)