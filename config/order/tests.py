from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from cart.models import Cart, CartItem
from product.models import Product

from .models import OrderInquiry


class CheckoutTests(TestCase):
	def setUp(self):
		self.user = CustomUser.objects.create_user(
			username='customer',
			password='StrongPass123!',
			name='Customer',
			email='customer@example.com',
			phone_no='9876543210',
			is_email_verified=True,
		)
		self.product = Product.objects.create(
			name='Standard Cover',
			product_code='SC-001',
			price='1250.00',
			stock=5,
			is_available=True,
		)
		self.client.force_login(self.user)

	def test_checkout_creates_inquiry_and_clears_cart(self):
		cart = Cart.objects.create(user=self.user)
		CartItem.objects.create(cart=cart, product=self.product, quantity=2)

		response = self.client.post(reverse('order:checkout'), {
			'customer_name': 'Customer',
			'customer_phone': '9876543210',
			'customer_email': 'customer@example.com',
			'notes': 'Please confirm delivery timeline.',
		})

		inquiry = OrderInquiry.objects.get(user=self.user)
		self.assertRedirects(
			response,
			reverse('order:success', args=[inquiry.inquiry_id]),
		)
		self.assertIn('Standard Cover (SC-001) x 2', inquiry.notes)
		self.assertIn('Please confirm delivery timeline.', inquiry.notes)
		self.assertFalse(CartItem.objects.filter(cart=cart).exists())

	def test_checkout_rejects_quantity_above_current_stock(self):
		cart = Cart.objects.create(user=self.user)
		CartItem.objects.create(cart=cart, product=self.product, quantity=6)

		response = self.client.post(reverse('order:checkout'), {
			'customer_name': 'Customer',
			'customer_phone': '9876543210',
			'customer_email': 'customer@example.com',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(OrderInquiry.objects.exists())
		self.assertTrue(CartItem.objects.filter(cart=cart).exists())
