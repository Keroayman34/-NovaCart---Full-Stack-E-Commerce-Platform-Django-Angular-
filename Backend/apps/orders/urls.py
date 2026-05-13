from django.urls import path
from .views import OrderListCreateView, OrderDetailView, CancelOrderView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='order-cancel'),
]