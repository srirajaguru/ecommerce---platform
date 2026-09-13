from django.contrib import admin

from .models import OrderInquiry


@admin.register(OrderInquiry)
class OrderInquiryAdmin(admin.ModelAdmin):
	list_display = ('inquiry_id', 'customer_name', 'customer_phone', 'status', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('inquiry_id', 'customer_name', 'customer_email', 'customer_phone')
	readonly_fields = ('inquiry_id', 'user', 'created_at', 'updated_at')
