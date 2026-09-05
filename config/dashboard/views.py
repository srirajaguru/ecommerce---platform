from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import render

from product.models import Product
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