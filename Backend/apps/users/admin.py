from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'role', 'is_verified', 'is_staff']
    list_filter = ['role', 'is_verified', 'is_staff']
    ordering = ['email']
    search_fields = ['email', 'phone']

    fieldsets = (
        ('Login Information', {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('phone', 'avatar')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'phone', 'is_verified'),
        }),
    )