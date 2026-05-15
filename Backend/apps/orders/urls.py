from django.urls import path

from .views import CancelOrderView, OrderDetailView, OrderListCreateView, OrderStatusUpdateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/cancel/', CancelOrderView.as_view(), name='order-cancel'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]
