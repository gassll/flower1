from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'full_name',
        'phone',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'full_name',
        'phone',
        'email',
    )

    list_editable = (
        'role',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': (
                'full_name',
                'phone',
                'role',
            )
        }),
    )