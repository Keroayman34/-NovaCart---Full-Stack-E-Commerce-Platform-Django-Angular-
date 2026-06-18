from django.urls import path
from .views import SellerProfileView

urlpatterns = [
    path('profile/', SellerProfileView.as_view(), name='seller-profile'),
    path('products/', SellerProfileView.as_view(), name='seller-products'),
    path('products/<int:pk>/', SellerProfileView.as_view(), name='seller-product-detail'),
    path('products/<int:pk>/delete/', SellerProfileView.as_view(), name='seller-product-delete'),
    path('products/<int:pk>/update/', SellerProfileView.as_view(), name='seller-product-update'),
    path('products/create/', SellerProfileView.as_view(), name='seller-product-create'),
]