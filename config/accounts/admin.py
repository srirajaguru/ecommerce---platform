from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # Users shown in the user list
    list_display = (
        'username',
        'email',
        'name',
        'phone_no',
        'is_email_verified',
        'is_staff',
        'is_active',
    )

    # Filters on the right side
    list_filter = (
        'is_email_verified',
        'is_staff',
        'is_active',
    )

    # Search box
    search_fields = (
        'username',
        'email',
        'name',
        'phone_no',
    )

    # Ordering
    ordering = ('username',)

    # Fields displayed when editing a user
    fieldsets = UserAdmin.fieldsets + (
        (
            'Customer Information',
            {
                'fields': (
                    'name',
                    'phone_no',
                    'is_email_verified',
                )
            },
        ),
    )

    # Fields displayed when creating a user from admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Customer Information',
            {
                'fields': (
                    'name',
                    'email',
                    'phone_no',
                    'is_email_verified',
                )
            },
        ),
    )