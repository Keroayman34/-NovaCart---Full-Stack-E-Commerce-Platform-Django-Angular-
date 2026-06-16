from django.urls import path

from .views.users import AdminUserListView, AdminUserUpdateView
from .views.products import AdminCategoryCreateView, AdminCategoryDetailView, AdminProductSoftDeleteView
from .views.orders import AdminOrderListView, AdminOrderUpdateView

app_name = 'admin_panel'

urlpatterns = [
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/', AdminUserUpdateView.as_view(), name='admin-user-update'),

    path('categories/', AdminCategoryCreateView.as_view(), name='admin-category-create'),
    path('categories/<int:pk>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
    path('products/<int:pk>/', AdminProductSoftDeleteView.as_view(), name='admin-product-soft-delete'),

    path('orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('orders/<int:pk>/', AdminOrderUpdateView.as_view(), name='admin-order-update'),
]
