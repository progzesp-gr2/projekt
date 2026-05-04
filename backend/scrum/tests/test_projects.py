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
        userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        cls.user = User.objects.create_user(**userdata)
    
    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create(self):
        projectdata: dict[str, Any] = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case'
        }

        response = self.client.post(path=reverse('project-list-create'), data=projectdata)
        self.assertEqual(response['content-type'], 'application/json')
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
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()

        for key, value in projectdata.items():
            self.assertEqual(rd[key], value)

        project = Project.objects.get(pk=1)
        projectdata['owner_id'] = projectdata['owner']
        del projectdata['owner']

        for key, value in projectdata.items():
            self.assertEqual(project.__dict__[key], value)
    
    def test_missing(self):
        response = self.client.post(path=reverse('project-list-create'))
        self.assertEqual(response.status_code, 400)

    def test_create_with_different_owner(self):
        projectdata = {
            'name': 'Test project',
            'key': 'test',
            'description': 'Project for a test case',
            'owner': 2
        }

        response = self.client.post(path=reverse('project-list-create'), data=projectdata)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
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
        self.client.force_login(self.user)

        response = self.client.get(path=reverse('project-list-create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        
        self.assertIsInstance(rd, list)

        for proj in rd:
            match proj['key']:
                case 'foo':
                    self.assertEqual(proj['name'], 'Foo')
                    self.assertEqual(proj['description'], 'Lorem ipsum dolor sit amet')
                case 'bar':
                    self.assertEqual(proj['name'], 'Bar')
                    self.assertEqual(proj['description'], 'zzzzz')
                case _:
                    self.fail()