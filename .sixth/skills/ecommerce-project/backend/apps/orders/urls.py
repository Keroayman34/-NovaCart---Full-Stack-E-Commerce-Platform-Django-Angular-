from django.urls import path

from .views import OrderStatusUpdateView, PlaceOrderView

urlpatterns = [
	path("", PlaceOrderView.as_view(), name="place-order"),
	path("<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status-update"),
]
