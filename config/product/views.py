from django.shortcuts import get_object_or_404, render

from .models import Product


def product_detail(request, product_id):
	product = get_object_or_404(
		Product,
		id=product_id,
		is_available=True
	)

	return render(
		request,
		'product/detail.html',
		{'product': product}
	)
