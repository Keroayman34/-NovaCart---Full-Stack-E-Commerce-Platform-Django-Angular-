"""Custom throttle classes for cart APIs."""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class CartUserThrottle(UserRateThrottle):
    """Rate throttle for authenticated cart users."""

    scope = "cart_user"


class CartAnonThrottle(AnonRateThrottle):
    """Rate throttle for anonymous cart users."""

    scope = "cart_anon"
