from django.urls import path

from .views import WishlistView

urlpatterns = [
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>/', WishlistView.as_view(), name='wishlist-remove'),
]
