"""Admin registrations for cart models."""

from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "coupon_code", "created_at", "updated_at")
    search_fields = ("session_key", "coupon_code", "user__email")
    list_filter = ("created_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    search_fields = ("product__name", "product__sku")
    list_filter = ("quantity",)

