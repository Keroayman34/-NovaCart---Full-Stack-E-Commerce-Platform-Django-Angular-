"""Serializers for cart APIs."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.db.models import F, Sum
from rest_framework import serializers

from apps.products.models import Product

from .models import Cart, CartItem


class ProductInCartSerializer(serializers.ModelSerializer):
    """Minimal nested product representation for cart responses."""

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "stock_quantity", "is_active"]
        read_only_fields = fields


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item with nested product and calculated line subtotal."""

    product = ProductInCartSerializer(read_only=True)
    line_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "line_subtotal"]

    def get_line_subtotal(self, obj: CartItem) -> Decimal:
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer including calculated totals."""

    items = CartItemSerializer(many=True, read_only=True)

    subtotal = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    shipping = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "coupon_code",
            "created_at",
            "updated_at",
            "items",
            "subtotal",
            "tax",
            "shipping",
            "total",
        ]

    def _totals(self) -> dict[str, Decimal]:
        cart: Cart = self.instance
        subtotal = (
            cart.items.select_related("product")
            .aggregate(sum_subtotal=Sum(F("product__price") * F("quantity")))
            .get("sum_subtotal")
        )
        subtotal = subtotal or Decimal("0")
        tax = subtotal * Decimal("0.14")
        shipping = Decimal("0") if subtotal > Decimal("1000") else Decimal("50")
        total = subtotal + tax + shipping
        return {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": total,
        }

    def get_subtotal(self, obj: Cart) -> Decimal:
        return self._totals()["subtotal"]

    def get_tax(self, obj: Cart) -> Decimal:
        return self._totals()["tax"]

    def get_shipping(self, obj: Cart) -> Decimal:
        return self._totals()["shipping"]

    def get_total(self, obj: Cart) -> Decimal:
        return self._totals()["total"]


class AddToCartSerializer(serializers.Serializer):
    """Validate add-to-cart request."""

    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Validate quantity update request."""

    quantity = serializers.IntegerField(min_value=1)


