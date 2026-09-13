from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart

from .forms import OrderInquiryForm
from .models import OrderInquiry

@login_required(login_url='login')
def checkout(request):
	cart = get_object_or_404(Cart.objects.prefetch_related('items__product'), user=request.user)
	items = list(cart.items.all())
	if not items:
		messages.info(request, 'Add a product to your cart before checking out.')
		return redirect('home')

	if request.method == 'POST':
		form = OrderInquiryForm(request.POST)
		if form.is_valid():
			with transaction.atomic():
				for item in items:
					item.product.refresh_from_db(fields=['stock', 'is_available'])
					if not item.product.is_available or item.quantity > item.product.stock:
						form.add_error(None, f'{item.product.name} is no longer available in that quantity.')
						break
				else:
					inquiry = form.save(commit=False)
					inquiry.user = request.user
					inquiry.save()
					item_lines = [
						f'- {item.product.name} ({item.product.product_code}) x {item.quantity}'
						for item in items
					]
					inquiry.notes = '\n'.join(item_lines) + (
						f'\n\nCustomer notes:\n{inquiry.notes}' if inquiry.notes else ''
					)
					inquiry.save(update_fields=['notes', 'updated_at'])
					cart.items.all().delete()
					return redirect('order:success', inquiry_id=inquiry.inquiry_id)
	else:
		form = OrderInquiryForm(initial={
			'customer_name': request.user.name or request.user.username,
			'customer_phone': request.user.phone_no or '',
			'customer_email': request.user.email,
		})

	return render(request, 'order/checkout.html', {'form': form, 'items': items})


@login_required(login_url='login')
def inquiry_success(request, inquiry_id):
	inquiry = get_object_or_404(OrderInquiry, inquiry_id=inquiry_id, user=request.user)
	whatsapp_text = (
		f'Hello, I submitted inquiry {inquiry.inquiry_id} for Sri Annai Precast.\n'
		f'Customer: {inquiry.customer_name}\n{inquiry.notes}'
	)
	whatsapp_url = (
		f'https://wa.me/{settings.COMPANY_WHATSAPP_NUMBER}'
		f'?text={quote(whatsapp_text)}'
	)
	return render(request, 'order/success.html', {
		'inquiry': inquiry,
		'whatsapp_url': whatsapp_url,
	})
