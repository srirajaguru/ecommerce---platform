from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from product.models import Product

from .models import Cart, CartItem


@login_required(login_url='login')
def add_to_cart(request, product_id):
	if request.method != 'POST':
		return redirect('home')

	product = get_object_or_404(
		Product,
		id=product_id,
		is_available=True
	)

	if product.stock < 1:
		messages.error(request, f'{product.name} is currently out of stock.')
		return redirect('home')

	cart, _ = Cart.objects.get_or_create(user=request.user)
	item, created = CartItem.objects.get_or_create(
		cart=cart,
		product=product,
		defaults={'quantity': 1}
	)

	if not created:
		if item.quantity < product.stock:
			item.quantity += 1
			item.save(update_fields=['quantity', 'updated_at'])
		else:
			messages.info(request, f'You have reached the available stock for {product.name}.')
			return redirect('home')

	messages.success(request, f'{product.name} was added to your cart.')
	return redirect('home')


@login_required(login_url='login')
def buy_now(request, product_id):
	if request.method != 'POST':
		return redirect('home')

	product = get_object_or_404(
		Product,
		id=product_id,
		is_available=True
	)

	if product.stock < 1:
		messages.error(request, f'{product.name} is currently out of stock.')
		return redirect('home')

	customer_name = request.user.name or request.user.username
	price = f'₹{product.price:.2f}' if product.price else 'Price on request'
	message = (
		f'Hello, I would like to buy this product.\n'
		f'Product: {product.name}\n'
		f'Code: {product.product_code}\n'
		f'Price: {price}\n'
		f'Customer: {customer_name}\n'
		f'Username: {request.user.username}'
	)
	whatsapp_url = (
		f'https://wa.me/{settings.COMPANY_WHATSAPP_NUMBER}'
		f'?text={quote(message)}'
	)

	return redirect(whatsapp_url)


@login_required(login_url='login')
def cart_detail(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)
	items = cart.items.select_related('product')

	return render(
		request,
		'cart/cart.html',
		{
			'cart': cart,
			'items': items,
		}
	)


@login_required(login_url='login')
def update_cart_item(request, item_id):
	if request.method != 'POST':
		return redirect('cart:detail')

	item = get_object_or_404(
		CartItem,
		id=item_id,
		cart__user=request.user,
	)
	try:
		quantity = int(request.POST.get('quantity', 0))
	except (TypeError, ValueError):
		quantity = 0

	if quantity <= 0:
		item.delete()
		messages.info(request, f'{item.product.name} was removed from your cart.')
	elif quantity > item.product.stock:
		messages.error(request, f'Only {item.product.stock} units of {item.product.name} are available.')
	else:
		item.quantity = quantity
		item.save(update_fields=['quantity', 'updated_at'])
		messages.success(request, 'Cart updated.')

	return redirect('cart:detail')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
	if request.method == 'POST':
		item = get_object_or_404(
			CartItem,
			id=item_id,
			cart__user=request.user,
		)
		name = item.product.name
		item.delete()
		messages.info(request, f'{name} was removed from your cart.')
	return redirect('cart:detail')
