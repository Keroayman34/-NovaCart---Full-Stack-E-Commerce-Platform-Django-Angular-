from django.urls import path

from .views import ReviewDeleteView, ReviewListCreateView

urlpatterns = [
    path('products/<int:product_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
]
