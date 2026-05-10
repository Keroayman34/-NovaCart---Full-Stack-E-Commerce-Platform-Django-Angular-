"""
Django admin configuration for products app.
"""
from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ("id", "name", "slug", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description")
        }),
        ("Media", {
            "fields": ("image",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


class ProductImageInline(admin.TabularInline):
    """Inline admin for ProductImage model."""
    model = ProductImage
    extra = 1
    fields = ("image", "is_primary", "alt_text", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = (
        "id",
        "name",
        "sku",
        "category",
        "seller",
        "price",
        "stock_quantity",
        "is_in_stock",
        "is_active",
        "is_deleted",
        "created_at",
    )
    list_filter = (
        "category",
        "seller",
        "is_active",
        "is_deleted",
        "created_at",
        "price",
    )
    search_fields = ("name", "slug", "sku", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("slug", "created_at", "updated_at")
    inlines = [ProductImageInline]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description", "category", "seller")
        }),
        ("Inventory", {
            "fields": ("sku", "price", "stock_quantity", "is_in_stock")
        }),
        ("Status", {
            "fields": ("is_active", "is_deleted")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related("category", "seller")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for ProductImage model."""
    list_display = ("id", "product", "is_primary", "created_at")
    list_filter = ("is_primary", "product__category", "created_at")
    search_fields = ("product__name", "product__sku", "alt_text")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Product", {
            "fields": ("product",)
        }),
        ("Image", {
            "fields": ("image", "alt_text")
        }),
        ("Settings", {
            "fields": ("is_primary",)
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related("product")
