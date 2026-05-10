from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	model = User
	list_display = ("email", "username", "role", "is_verified", "is_staff")
	list_filter = ("role", "is_verified", "is_staff")
	ordering = ("email",)
	search_fields = ("email", "username")
	fieldsets = UserAdmin.fieldsets + (
		("Profile", {"fields": ("role", "is_verified")}),
	)
