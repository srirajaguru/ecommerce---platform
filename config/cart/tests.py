from django.urls import reverse
from django.test import TestCase

from accounts.models import CustomUser
from product.models import Product


class BuyNowTests(TestCase):
	def test_buy_now_redirects_to_company_whatsapp(self):
		user = CustomUser.objects.create_user(
			username='customer',
			password='StrongPass123!',
			name='Customer',
			email='customer@example.com',
			is_email_verified=True,
		)
		product = Product.objects.create(
			name='Standard Cover',
			product_code='SC-001',
			price='1250.00',
			stock=5,
			is_available=True,
		)
		self.client.force_login(user)

		response = self.client.post(
			reverse('cart:buy_now', args=[product.id])
		)

		self.assertEqual(response.status_code, 302)
		self.assertIn('https://wa.me/918344318967?text=', response.url)
		self.assertIn('Standard%20Cover', response.url)
