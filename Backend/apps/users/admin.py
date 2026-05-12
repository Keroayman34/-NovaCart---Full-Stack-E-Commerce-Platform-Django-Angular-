from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("role",)}),
    )