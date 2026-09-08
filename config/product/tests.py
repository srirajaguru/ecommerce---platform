from django.urls import reverse
from django.test import TestCase

from .models import Product


class ProductDetailTests(TestCase):
	def test_product_detail_displays_available_product(self):
		product = Product.objects.create(
			name='Standard Cover',
			product_code='SC-001',
			description='A durable cover.',
			stock=5,
			is_available=True,
		)

		response = self.client.get(
			reverse('product:detail', args=[product.id])
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, product.name)

	def test_product_detail_hides_unavailable_product(self):
		product = Product.objects.create(
			name='Unavailable Cover',
			product_code='UC-001',
			stock=0,
			is_available=False,
		)

		response = self.client.get(
			reverse('product:detail', args=[product.id])
		)

		self.assertEqual(response.status_code, 404)
