from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, ProjectMembership

User = get_user_model()

class ApiProjectMembershipCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.users = [
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com'),
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
            User.objects.create_user(username='jkow', password='1234', first_name='Jan', last_name='Kowalski', email='jkow@example.com')
        ]

        cls.project = Project.objects.create(name='Foo', key='foo', description='Lorem ipsum dolor sit amet', owner=cls.users[0])
        ProjectMembership.objects.create(project=cls.project, user=cls.users[1], role=ProjectMembership.ProjectRole.SCRUM_MASTER)

    def test_create(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[2].pk,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 201)
        rd = response.json()
        memb = ProjectMembership.objects.get(pk=rd['id'])

        self.assertEqual(memb.project, self.project)
        for k, v in data.items():
            self.assertEqual(rd[k], v)

    def test_no_permission(self):
        self.client.force_login(self.users[1])

        data = {
            'user': self.users[2].pk,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 403)
    
    def test_invisible(self):
        self.client.force_login(self.users[2])

        data = {
            'user': self.users[2].pk,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 404)

    def test_add_owner(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[0].pk,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)
    
    def test_add_existing(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[1].pk,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)
    
    def test_add_second_master(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[2].pk,
            'role': 'SCRUM_MASTER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)
    
    def test_add_product_owner(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[2].pk,
            'role': 'PRODUCT_OWNER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)
    
    def test_bad_role(self):
        self.client.force_login(self.users[0])

        data = {
            'user': self.users[2].pk,
            'role': 'ZZZZ'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)
    
    def test_bad_user(self):
        self.client.force_login(self.users[0])

        data = {
            'user': 9999,
            'role': 'PROGRAMMER'
        }

        response = self.client.post(
            path=reverse('project-membership-list-create', args=[self.project.pk]),
            data=data
        )

        self.assertEqual(response.status_code, 400)

class ApiProjectMembershipListTestCase(TestCase):
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
            Project.objects.create(name='Bar', key='bar', description='zzzzz', owner=cls.users[0]),
            Project.objects.create(name='Baz', key='baz', description='zzzzz', owner=cls.users[0])
        ]
        cls.memberships = [
            ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[1], role=ProjectMembership.ProjectRole.SCRUM_MASTER),
            ProjectMembership.objects.create(project=cls.projects[0], user=cls.users[2], role=ProjectMembership.ProjectRole.PROGRAMMER),
            ProjectMembership.objects.create(project=cls.projects[1], user=cls.users[3], role=ProjectMembership.ProjectRole.PROGRAMMER)
        ]
    
    def test_get_list(self):
        self.client.force_login(self.users[0])

        response = self.client.get(path=reverse('project-membership-list-create', args=[self.projects[0].pk]))
        rd = response.json()

        for m in rd:
            if m['id'] == self.memberships[0].pk:
                self.assertEqual(m['project'], self.projects[0].pk)
                self.assertEqual(m['user'], self.users[1].pk)
                self.assertEqual(m['user_details']['id'], self.users[1].pk)
                self.assertEqual(m['role'], 'SCRUM_MASTER')
            elif m['id'] == self.memberships[1].pk:
                self.assertEqual(m['project'], self.projects[0].pk)
                self.assertEqual(m['user'], self.users[2].pk)
                self.assertEqual(m['user_details']['id'], self.users[2].pk)
                self.assertEqual(m['role'], 'PROGRAMMER')
            elif m['id'] == self.memberships[2].pk:
                self.assertEqual(m['project'], self.projects[1].pk)
                self.assertEqual(m['user'], self.users[3].pk)
                self.assertEqual(m['user_details']['id'], self.users[3].pk)
                self.assertEqual(m['role'], 'PROGRAMMER')
            else:
                self.fail()

    def test_not_owner(self):
        self.client.force_login(self.users[3])

        response = self.client.get(path=reverse('project-membership-list-create', args=[self.projects[1].pk]))
        rd = response.json()

        self.assertEqual(len(rd), 1)
        self.assertEqual(rd[0]['id'], self.memberships[2].pk)

    def test_invisible(self):
        self.client.force_login(self.users[3])

        response = self.client.get(path=reverse('project-membership-list-create', args=[self.projects[2].pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_missing(self):
        self.client.force_login(self.users[3])

        response = self.client.get(path=reverse('project-membership-list-create', args=[9999]))
        self.assertEqual(response.status_code, 404)