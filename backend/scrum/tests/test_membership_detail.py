from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, ProjectMembership

User = get_user_model()

class ApiProjectMembershipGetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
            User.objects.create_user(username='jkow', password='1234', first_name='Jan', last_name='Kowalski', email='jkow@example.com'),
            User.objects.create_user(username='stw', password='5678', first_name='Stanisław', last_name='Twaróg', email='stw@example.com')
        ]

        cls.projects = [
            Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0]),
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.users[0])
        ]
        cls.memberships = [
            ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[1], role=ProjectMembership.ProjectRole.SCRUM_MASTER),
            ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[2], role=ProjectMembership.ProjectRole.PROGRAMMER),
            ProjectMembership.objects.create(project=cls.projects[1], user=cls.users[3], role=ProjectMembership.ProjectRole.PROGRAMMER)
        ]
    
    def test_get(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('project-membership-detail', args=[self.projects[0].pk, self.memberships[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        
        expect = {
            'id': self.memberships[0].pk,
            'project': self.projects[0].pk,
            'user': self.users[1].pk,
            'role': 'SCRUM_MASTER'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
        
        expect = {
            "username": "tp",
            "first_name": "Tomasz",
            "last_name": "Problem",
            "email": "tp@example.com",
        }

        for key, value in expect.items():
            self.assertEqual(rd['user_details'][key], value)
    
    def test_get_not_owner(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('project-membership-detail', args=[self.projects[0].pk, self.memberships[0].pk]))

        self.assertEqual(response.status_code, 200)

        rd = response.json()

        expect = {
            'id': self.memberships[0].pk,
            'project': self.projects[0].pk,
            'user': self.users[1].pk,
            'role': 'SCRUM_MASTER'
        }

        for key, value in expect.items():
            self.assertEqual(rd[key], value)
        
        expect = {
            "username": "tp",
            "first_name": "Tomasz",
            "last_name": "Problem",
            "email": "tp@example.com",
        }

        for key, value in expect.items():
            self.assertEqual(rd['user_details'][key], value)

    def test_get_invisible(self):
        self.client.force_login(self.users[1])

        response = self.client.get(path=reverse('project-membership-detail', args=[self.projects[1].pk, self.memberships[2].pk]))

        self.assertEqual(response.status_code, 404)
    
    def test_get_missing(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('project-membership-detail', args=[self.projects[0].pk, 999]))

        self.assertEqual(response.status_code, 404)

class ApiProjectMembershipUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
            User.objects.create_user(username='jkow', password='1234', first_name='Jan', last_name='Kowalski', email='jkow@example.com')
        ]

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        cls.membership = ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.SCRUM_MASTER)
    
    def test_update_role(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'role': 'PROGRAMMER'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        self.assertEqual(rd['role'], 'PROGRAMMER')
        self.assertEqual(ProjectMembership.objects.get(pk=self.membership.pk).role, 'PROGRAMMER')

    def test_update_user(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'user': self.users[2].pk},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        rd = response.json()
        self.assertEqual(rd['user'], self.users[2].pk)
        self.assertEqual(ProjectMembership.objects.get(pk=self.membership.pk).role, 'SCRUM_MASTER')
        self.assertEqual(ProjectMembership.objects.get(pk=self.membership.pk).user, self.users[2])
        self.assertEqual(rd['user_details']['id'], self.users[2].pk)
    
    def test_bad_role(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'role': 'ZZZZ'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_bad_user(self):
        self.client.force_login(self.users[0])

        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'user': 9999},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
    
    def test_no_permission(self):
        self.client.force_login(self.users[1])
        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'role': 'PROGRAMMER'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_invisible(self):
        self.client.force_login(self.users[2])
        response = self.client.patch(
            path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]),
            data={'role': 'PROGRAMMER'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
    
class ApiProjectMembershipDeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
            User.objects.create_user(username='jkow', password='1234', first_name='Jan', last_name='Kowalski', email='jkow@example.com')
        ]

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        cls.membership = ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.SCRUM_MASTER)
    
    def test_delete(self):
        self.client.force_login(self.users[0])

        response = self.client.delete(path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]))

        self.assertEqual(response.status_code, 204)

        self.assertFalse(ProjectMembership.objects.contains(self.membership))
    
    def test_no_permission(self):
        self.client.force_login(self.users[1])
        response = self.client.delete(path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(ProjectMembership.objects.contains(self.membership))

    def test_invisible(self):
        self.client.force_login(self.users[2])
        response = self.client.delete(path=reverse('project-membership-detail', args=[self.project.pk, self.membership.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ProjectMembership.objects.contains(self.membership))