from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'email',
        'name',
        'phone_no',
        'is_email_verified',
        'is_staff',
        'is_active',
    )