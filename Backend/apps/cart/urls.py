from django.urls import path
from .views import CartView, CartItemView, ClearCartView, MergeCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
    path('cart/merge/', MergeCartView.as_view(), name='cart-merge'),
    path('cart/<int:pk>/', CartItemView.as_view(), name='cart-item'),
]