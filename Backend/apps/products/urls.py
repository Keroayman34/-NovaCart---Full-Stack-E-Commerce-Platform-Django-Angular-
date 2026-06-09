from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .admin_views import AdminCategoryCreateView, AdminCategoryDetailView, AdminProductSoftDeleteView
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

app_name = 'products'

urlpatterns = [
    path('', include(router.urls)),
    path('admin/categories/', AdminCategoryCreateView.as_view(), name='admin-category-create'),
    path('admin/categories/<int:pk>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
    path('admin/products/<int:pk>/', AdminProductSoftDeleteView.as_view(), name='admin-product-soft-delete'),
]
