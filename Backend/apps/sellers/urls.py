from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', SellerProfileView.as_view(), name='seller-profile'),
    path('products/', SellerOwnerProductListView.as_view(), name='seller-products'),
    path('products/<int:pk>/', SellerOwnerProductDetailView.as_view(), name='seller-product-detail'),
    path('products/<int:pk>/delete/', SellerOwnerProductDeleteView.as_view(), name='seller-product-delete'),
    path('products/<int:pk>/update/', SellerOwnerProductUpdateView.as_view(), name='seller-product-update'),
    path('products/create/', SellerOwnerProductCreateView.as_view(), name='seller-product-create'),
    path('dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
]