from django.urls import path

from .views import WishlistListView, WishlistAddView, WishlistRemoveView

urlpatterns = [
	path("", WishlistListView.as_view(), name="wishlist-list"),
	path("add/", WishlistAddView.as_view(), name="wishlist-add"),
	path("<int:pk>/", WishlistRemoveView.as_view(), name="wishlist-remove"),
]
