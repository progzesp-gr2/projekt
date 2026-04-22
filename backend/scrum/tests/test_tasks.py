from ..models import Project, Sprint, Task
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse

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
        cls.userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**cls.userdata)
        del cls.userdata['password']
        
        cls.projectdata = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case',
            'owner': cls.user
        }

        cls.project = Project.objects.create(**cls.projectdata)
    
    def setUp(self) -> None:
        self.assertTrue(self.client.login(username='jtp', password='pass'))

    def test_create(self):
        taskdata = {
            'title': 'Test Task',
            'project': 1
        }

        response = self.client.post(path=reverse('task-list-create'), data=taskdata)
        rd = response.json()

        self.assertEqual(response.status_code, 201)

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
        rd = response.json()

        self.assertEqual(response.status_code, 201)

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

    def test_create_with_diffrent_reporter(self):
        taskdata = {
            'title': 'Test Task',
            'project': 1,
            'reporter': 2
        }

        response = self.client.post(path=reverse('task-list-create'), data=taskdata)

        rd = response.json()
        task = Task.objects.get(pk=rd['id'])

        self.assertEqual(rd['reporter'], 1)
        self.assertEqual(task.reporter, self.user)