from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        'username',
        'full_name',
        'phone',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('full_name', 'phone', 'role')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'full_name',
                'phone',
                'email',
                'role',
                'password1',
                'password2',
            ),
        }),
    )