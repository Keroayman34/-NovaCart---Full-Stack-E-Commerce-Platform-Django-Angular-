from django.urls import path

from .admin_views import AdminCategoryCreateView, AdminCategoryDetailView, AdminProductSoftDeleteView

urlpatterns = [
    path("admin/categories/", AdminCategoryCreateView.as_view(), name="admin-category-create"),
    path("admin/categories/<int:pk>/", AdminCategoryDetailView.as_view(), name="admin-category-detail"),
    path("admin/products/<int:pk>/", AdminProductSoftDeleteView.as_view(), name="admin-product-soft-delete"),
]
