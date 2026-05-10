from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, ProjectMembership, Sprint
from datetime import date

User = get_user_model()

class ApiProjectGetTestCase(TestCase):
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
    
    def test_get(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('project-detail', args=[self.projects[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        
        expect = {
            'id': self.projects[0].pk,
            'name': 'Foo',
            'key': 'foo',
            'description': 'Lorem ipsum dolor sit amet',
            'owner': self.users[0].pk
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
    
    def test_get_not_owner(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('project-detail', args=[self.projects[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.projects[0].pk,
            'name': 'Foo',
            'key': 'foo',
            'description': 'Lorem ipsum dolor sit amet',
            'owner': self.users[0].pk
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)

    def test_get_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('project-detail', args=[self.projects[1].pk]))

        self.assertEqual(response.status_code, 404)
    
    def test_get_missing(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('project-detail', args=[999]))

        self.assertEqual(response.status_code, 404)

class ApiProjectUpdateTestCase(TestCase):
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
    
    def test_update(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-detail', args=[self.projects[0].pk]), 
            data={'description': 'changed'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.get(pk=self.projects[0].pk).description, 'changed')

        rd = response.json()

        expect = {
            'id': self.projects[0].pk,
            'name': 'Foo',
            'key': 'foo',
            'description': 'changed',
            'owner': self.users[0].pk
        }

        for k, v in expect.items():
            self.assertEqual(rd[k], v)
    
    def test_change_owner(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-detail', args=[self.projects[0].pk]), 
            data={'owner': self.users[1].pk},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.get(pk=self.projects[0].pk).owner, self.users[1])

        rd = response.json()

        expect = {
            'id': self.projects[0].pk,
            'name': 'Foo',
            'key': 'foo',
            'description': 'Lorem ipsum dolor sit amet',
            'owner': self.users[1].pk
        }

        for k, v in expect.items():
            self.assertEqual(rd[k], v)

    def test_change_owner_bad(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-detail', args=[self.projects[1].pk]), 
            data={'owner': self.users[1].pk},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_update_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.patch(
            path=reverse('project-detail', args=[self.projects[0].pk]), 
            data={'owner': self.users[1].pk},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
    
    def test_update_empty(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-detail', args=[self.projects[0].pk]), 
            data={},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.projects[0].pk,
            'name': 'Foo',
            'key': 'foo',
            'description': 'Lorem ipsum dolor sit amet',
            'owner': self.users[0].pk
        }

        for k, v in expect.items():
            self.assertEqual(rd[k], v)

class ApiProjectDeleteTestCase(TestCase):
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
    
    def test_delete(self):
        self.client.force_login(self.users[0])

        response = self.client.delete(path=reverse('project-detail', args=[self.project.pk]))

        self.assertEqual(response.status_code, 204)

        self.assertFalse(Project.objects.contains(self.project))
        self.assertFalse(Sprint.objects.contains(self.sprint))

    def test_delete_no_permission(self):
        self.client.force_login(self.users[1])

        response = self.client.delete(path=reverse('project-detail', args=[self.project.pk]))

        self.assertEqual(response.status_code, 404)

        self.assertTrue(Project.objects.contains(self.project))
        self.assertTrue(Sprint.objects.contains(self.sprint))