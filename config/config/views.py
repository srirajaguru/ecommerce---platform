from django.shortcuts import render

from product.models import Product


def home(request):
    products = Product.objects.filter(
        is_available=True
    ).order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'products': products,
        }
    )


def services(request):
    return render(request, 'services.html')