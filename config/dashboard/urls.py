from django.urls import path

from . import views


urlpatterns = [

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),
    path(
        'dashboard/products/',
        views.products_view,
        name='dashboard_products'
    ),
    path(
        'dashboard/products/add/',
        views.product_add_view,
        name='dashboard_product_add'
    ),
    path(
        'dashboard/customers/',
        views.customers_view,
        name='dashboard_customers'
    ),
    path(
        'dashboard/inquiries/',
        views.inquiries_view,
        name='dashboard_inquiries'
    ),
    path(
        'dashboard/analytics/',
        views.analytics_view,
        name='dashboard_analytics'
    ),

]