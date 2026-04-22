from typing import Any

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, get_user
from ..models import Project

User = get_user_model()

class ApiProjectNoLoginTestCase(TestCase):
    def test_nologin(self):
        response = self.client.get(path=reverse('project-list-create'))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(path=reverse('project-list-create'))
        self.assertEqual(response.status_code, 403)


class ApiProjectCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**cls.userdata)
        del cls.userdata['password']
    
    def setUp(self) -> None:
        self.assertTrue(self.client.login(username='jtp', password='pass'))

    def test_create(self):
        # self.client.login(username='jtp', password='pass')

        projectdata: dict[str, Any] = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case'
        }

        response = self.client.post(path=reverse('project-list-create'), data=projectdata)
        rd = response.json()

        self.assertEqual(response.status_code, 201)

        projectdata['owner'] = get_user(self.client).pk

        for key, value in projectdata.items():
            self.assertEqual(rd[key], value)

        project = Project.objects.get(pk=1)
        projectdata['owner_id'] = projectdata['owner']
        del projectdata['owner']

        for key, value in projectdata.items():
            self.assertEqual(project.__dict__[key], value)

    def test_create_with_owner(self):
        projectdata = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case',
            'owner': 1
        }

        response = self.client.post(path=reverse('project-list-create'), data=projectdata)
        rd = response.json()

        self.assertEqual(response.status_code, 201)

        project = Project.objects.get(pk=1)
        projectdata['owner_id'] = projectdata['owner']
        del projectdata['owner']

        for key, value in projectdata.items():
            self.assertEqual(project.__dict__[key], value)
    
    def test_missing(self):
        response = self.client.post(path=reverse('project-list-create'))
        self.assertEqual(response.status_code, 400)

    def test_create_with_diffrent_owner(self):
        projectdata = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case',
            'owner': 2
        }

        response = self.client.post(path=reverse('project-list-create'), data=projectdata)
        rd = response.json()
        project = Project.objects.get(pk=rd['id'])

        self.assertEqual(rd['owner'], 1)
        self.assertEqual(project.owner, self.user)


class ApiProjectListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**cls.userdata)
        del cls.userdata['password']

        cls.projects = [
            Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.user),
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.user)
        ]
    
    def test_get_list(self):
        self.assertTrue(self.client.login(username='jtp', password='pass'))

        response = self.client.get(path=reverse('project-list-create'))
        
        self.assertEqual(response.status_code, 200)
        rd = response.json()
        
        self.assertTrue(isinstance(rd, list))

        cd = {}

        for p in rd:
            cd[p['key']] = (p['name'], p['description'])
        
        self.assertIn('foo', cd.keys())
        self.assertIn('bar', cd.keys())
        
        self.assertEqual(cd['foo'][0], 'Foo')
        self.assertEqual(cd['foo'][1], 'Lorem ipsum dolor sit amet')
        self.assertEqual(cd['bar'][0], 'Bar')
        self.assertEqual(cd['bar'][1], 'zzzzz')
