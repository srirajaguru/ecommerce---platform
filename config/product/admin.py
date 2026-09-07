from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'product_code',
		'price',
		'stock',
		'is_available',
	)
	list_filter = ('is_available', 'material')
	search_fields = ('name', 'product_code')
