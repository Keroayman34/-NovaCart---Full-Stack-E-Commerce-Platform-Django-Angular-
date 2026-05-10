from decimal import Decimal

import stripe
from django.conf import settings
from rest_framework import serializers


def _configure_stripe_api_key() -> None:
    secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    if not secret_key:
        raise serializers.ValidationError("Stripe secret key is not configured.")
    stripe.api_key = secret_key


def create_payment_intent(*, amount: Decimal, currency: str, metadata: dict | None = None):
    _configure_stripe_api_key()
    amount_in_cents = int(amount * 100)
    return stripe.PaymentIntent.create(
        amount=amount_in_cents,
        currency=currency,
        metadata=metadata or {},
    )


def retrieve_payment_intent(payment_intent_id: str):
    _configure_stripe_api_key()
    return stripe.PaymentIntent.retrieve(payment_intent_id)
