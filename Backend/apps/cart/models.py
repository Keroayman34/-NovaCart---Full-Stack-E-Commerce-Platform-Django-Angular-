"""Cart and CartItem models for NovaCart.

Architecture note:
- Business logic lives in services.py.
- Models only define persistence and basic constraints.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class Cart(models.Model):
    """Shopping cart.

    Supports:
    - Authenticated users via `user`
    - Guest users via `session_key`

    Constraints:
    - One active cart per user
    - One active cart per session_key for guests
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
        db_index=True,
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Django session key for guest carts",
    )
    coupon_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Optional coupon code",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["session_key", "created_at"]),
        ]
        constraints = [
            # Uniqueness for user carts (user is not null)
            models.UniqueConstraint(
                fields=["user"],
                condition=~models.Q(user=None),
                name="unique_active_cart_per_user",
            ),
            # Uniqueness for guest carts (session_key is not null)
            models.UniqueConstraint(
                fields=["session_key"],
                condition=~models.Q(session_key=None),
                name="unique_active_cart_per_session_key",
            ),
        ]

    def __str__(self) -> str:
        if self.user_id:
            return f"Cart(user_id={self.user_id})"
        return f"Cart(session_key={self.session_key})"


class CartItem(models.Model):
    """Cart line item."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
            )
        ]

    def __str__(self) -> str:
        return f"CartItem(cart_id={self.cart_id}, product_id={self.product_id})"

