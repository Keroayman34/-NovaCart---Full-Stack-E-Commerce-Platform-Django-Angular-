from django.urls import path

from .views import PaymentCreateView, StripePaymentConfirmView, StripePaymentIntentCreateView

urlpatterns = [
	path("", PaymentCreateView.as_view(), name="payment-create"),
	path("stripe/", StripePaymentIntentCreateView.as_view(), name="stripe-payment-intent"),
	path("stripe/confirm/", StripePaymentConfirmView.as_view(), name="stripe-payment-confirm"),
]
