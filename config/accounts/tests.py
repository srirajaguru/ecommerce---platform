from django.test import TestCase

from .models import CustomUser


class LoginDestinationTests(TestCase):
	def test_customer_login_redirects_to_home(self):
		CustomUser.objects.create_user(
			username='customer',
			password='StrongPass123!',
			name='Customer',
			email='customer@example.com',
			is_email_verified=True,
		)

		response = self.client.post(
			'/login/?next=/cart/',
			{
				'username': 'customer',
				'password': 'StrongPass123!',
			}
		)

		self.assertRedirects(response, '/')

	def test_staff_login_redirects_to_dashboard(self):
		CustomUser.objects.create_user(
			username='admin',
			password='StrongPass123!',
			name='Admin',
			email='admin@example.com',
			is_staff=True,
			is_email_verified=True,
		)

		response = self.client.post(
			'/login/',
			{
				'username': 'admin',
				'password': 'StrongPass123!',
			}
		)

		self.assertRedirects(response, '/dashboard/')
