from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('item/<int:item_id>/update/', views.update_cart_item, name='update_item'),
    path('item/<int:item_id>/remove/', views.remove_from_cart, name='remove_item'),
]