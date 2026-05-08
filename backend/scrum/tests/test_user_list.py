from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ApiUserListTestCase(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.users = [
            User.objects.create_user(username='tp', password='pw', first_name='Tomasz', last_name='Problem', email='tp@example.com'),
            User.objects.create_user(username='jtp', password='pass', first_name='Jan', last_name='Tępy', email='jtp@example.com')
        ]

	def test_get_list(self):
		self.client.force_login(self.users[0])

		response = self.client.get(path=reverse('user-list'))

		self.assertEqual(response.status_code, 200)
		rd = response.json()
		
		expect = [
			{
				'id': self.users[1].pk,
				'username': 'jtp',
				'first_name': 'Jan',
				'last_name': 'Tępy',
				'email': 'jtp@example.com'
			},
			{
				'id': self.users[0].pk,
				'username': 'tp',
				'first_name': 'Tomasz',
				'last_name': 'Problem',
				'email': 'tp@example.com'
			}
		]

		for exu, rdu in zip(expect, rd):
			for k, v in exu.items():
				self.assertIn(k, rdu)
				self.assertEqual(rdu[k], v)
	
	def test_nologin(self):
		response = self.client.get(path=reverse('user-list'))

		self.assertEqual(response.status_code, 403)