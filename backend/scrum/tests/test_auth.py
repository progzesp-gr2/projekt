from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse

User = get_user_model()

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
        self.assertEqual(rd['message'], 'User created successfully.')
        self.assertFalse(rd['user_exists'])
        self.assertTrue(rd['user_created'])
        for key, value in data.items():
            self.assertEqual(rd[key], value)
            self.assertEqual(user.__dict__[key], value)

    def test_create_existing_username(self):
        # Duplicate registration: the API reports that the user already exists
        # and does not create another database row.
        User.objects.create_user(username='jtp', password='pass')

        response = self.client.post(
            path=reverse('auth-register'),
            data={'username': 'jtp', 'password': 'test'}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        rd = response.json()
        self.assertEqual(rd['message'], 'User could not be created.')
        self.assertTrue(rd['user_exists'])
        self.assertFalse(rd['user_created'])
        self.assertIn('username', rd['errors'])
        self.assertEqual(User.objects.filter(username='jtp').count(), 1)

    def test_missing(self):
        response = self.client.post(path=reverse('auth-register'))

        self.assertEqual(response.status_code, 400)
        rd = response.json()
        # Verifies the registration failure payload for missing fields.
        self.assertEqual(rd['message'], 'User could not be created.')
        self.assertFalse(rd['user_exists'])
        self.assertFalse(rd['user_created'])
        self.assertIn('errors', rd)
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
        rd = response.json()
        self.assertEqual(rd['message'], 'Login successful.')
        self.assertTrue(rd['login_success'])
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
        rd = response.json()
        # Verifies the login failure payload for missing credentials.
        self.assertEqual(rd['message'], 'Username and password are required.')
        self.assertFalse(rd['login_success'])
        self.assertIn('errors', rd)
        response = self.client.post(path=reverse('auth-login'), data={'username': 'jtp'})
        self.assertEqual(response.status_code, 400)
        rd = response.json()
        self.assertEqual(rd['message'], 'Username and password are required.')
        self.assertFalse(rd['login_success'])
        self.assertIn('errors', rd)
    
    def test_bad_user(self):
        response = self.client.post(path=reverse('auth-login'), data={'username': 'nope', 'password': 'pass'})

        self.assertEqual(response.status_code, 400)
        rd = response.json()
        # Verifies the login failure payload for an unknown username.
        self.assertEqual(rd['message'], 'Invalid username or password.')
        self.assertFalse(rd['login_success'])

    def test_bad_password(self):
        response = self.client.post(path=reverse('auth-login'), data={'username': 'jtp', 'password': 'nope'})

        self.assertIn(response.status_code, (400, 401))
        rd = response.json()
        # Verifies the login failure payload for an incorrect password.
        self.assertEqual(rd['message'], 'Invalid username or password.')
        self.assertFalse(rd['login_success'])
