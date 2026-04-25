from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse

User = get_user_model()

# Create your tests here.

class ApiRegisterTestCase(TestCase):
    def test_create(self):
        data = {'username': 'jtp', 'password': 'test', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}

        response = self.client.post(
            path=reverse('auth-register'), 
            data=data
        )

        self.assertEqual(response.status_code, 201)

        del data['password']

        user = User.objects.get(pk=1)
        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        for key, value in data.items():
            self.assertEqual(rd[key], value)
            self.assertEqual(user.__dict__[key], value)

    def test_missing(self):
        response = self.client.post(path=reverse('auth-register'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)


class ApiAuthTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.userdata = {'username': 'jtp', 'password': 'pass', 'first_name': 'Jan', 'last_name': 'Tępy', 'email': 'jtp@example.com'}
        User.objects.create_user(**cls.userdata)
        del cls.userdata['password']

    def test_login(self):
        response = self.client.post(path=reverse('auth-login'), data={'username': 'jtp', 'password': 'pass'})

        self.assertEqual(response.status_code, 200)

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)
        for key, value in self.userdata.items():
            self.assertEqual(user.__dict__[key], value)
        
    def test_me(self):
        self.assertTrue(self.client.login(username='jtp', password='pass'))

        response = self.client.get(reverse('auth-me'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        for key, value in self.userdata.items():
            self.assertEqual(rd[key], value)

    def test_logout(self):
        self.assertTrue(self.client.login(username='jtp', password='pass'))

        response = self.client.post(reverse('auth-logout'))

        self.assertEqual(response.status_code, 204)

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
    
    def test_nologin(self):
        response = self.client.get(path=reverse('auth-me'))
        self.assertEqual(response.status_code, 403)

    def test_login_missing(self):
        response = self.client.post(path=reverse('auth-login'))
        self.assertEqual(response.status_code, 400)
        response = self.client.post(path=reverse('auth-login'), data={'username': 'jtp'})
        self.assertEqual(response.status_code, 400)
    
    def test_bad_user(self):
        response = self.client.post(path=reverse('auth-login'), data={'username': 'nope', 'password': 'pass'})

        self.assertEqual(response.status_code, 400)

    def test_bad_password(self):
        response = self.client.post(path=reverse('auth-login'), data={'username': 'jtp', 'password': 'nope'})

        self.assertIn(response.status_code, (400, 401))
