from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from product.models import Product
from product.forms import ProductForm
from order.models import OrderInquiry


User = get_user_model()


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='login')
def dashboard_view(request):

    # Customers
    total_users = User.objects.count()

    verified_users = User.objects.filter(
        is_email_verified=True
    ).count()

    # Products
    total_products = Product.objects.count()

    # Order Inquiries
    total_inquiries = OrderInquiry.objects.count()

    # Recent Customers
    recent_users = User.objects.order_by(
        '-date_joined'
    )[:5]

    # Recent Inquiries
    recent_inquiries = OrderInquiry.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )[:5]

    context = {
        'total_users': total_users,
        'verified_users': verified_users,
        'total_products': total_products,
        'total_inquiries': total_inquiries,
        'recent_users': recent_users,
        'recent_inquiries': recent_inquiries,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@user_passes_test(is_admin, login_url='login')
def products_view(request):
    products = Product.objects.order_by('name')
    return render(request, 'dashboard/products.html', {'products': products})


@user_passes_test(is_admin, login_url='login')
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_products')
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_add.html', {'form': form})


@user_passes_test(is_admin, login_url='login')
def customers_view(request):
    customers = User.objects.order_by('username')
    return render(request, 'dashboard/customers.html', {'customers': customers})


@user_passes_test(is_admin, login_url='login')
def inquiries_view(request):
    inquiries = OrderInquiry.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/inquiries.html', {'inquiries': inquiries})


@user_passes_test(is_admin, login_url='login')
def analytics_view(request):
    context = {
        'total_products': Product.objects.count(),
        'available_products': Product.objects.filter(is_available=True).count(),
        'total_customers': User.objects.count(),
        'verified_customers': User.objects.filter(is_email_verified=True).count(),
        'total_inquiries': OrderInquiry.objects.count(),
        'pending_inquiries': OrderInquiry.objects.filter(status='pending').count(),
        'contacted_inquiries': OrderInquiry.objects.filter(status='contacted').count(),
        'confirmed_inquiries': OrderInquiry.objects.filter(status='confirmed').count(),
        'cancelled_inquiries': OrderInquiry.objects.filter(status='cancelled').count(),
    }
    return render(request, 'dashboard/analytics.html', context)