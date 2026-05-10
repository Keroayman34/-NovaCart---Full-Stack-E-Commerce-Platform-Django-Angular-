"""Cart business logic for NovaCart.

Views must delegate to CartService.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.db.models import F, Sum, Prefetch

from apps.products.models import Product
from core.exceptions import (
    OutOfStockException,
    ProductInactiveException,
    InvalidQuantityException,
)

from .models import Cart, CartItem


class CartService:
    """Cart domain service."""

    TAX_RATE = Decimal("0.14")
    SHIPPING_FREE_THRESHOLD = Decimal("1000")
    SHIPPING_FEE = Decimal("50")

    @staticmethod
    def get_or_create_cart(request, *, session_key: str | None = None) -> Cart:
        """Get existing cart or create a new one.

        - Authenticated: cart is tied to user
        - Guest: cart is tied to session_key
        """

        if request.user and request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, defaults={})
            return cart

        if not request.session.session_key and session_key is None:
            request.session.save()

        sk = session_key or request.session.session_key
        if not sk:
            raise ValueError("Session key is required for guest cart.")

        cart, _ = Cart.objects.get_or_create(session_key=sk, defaults={})
        return cart

    @staticmethod
    def _validate_product_for_cart(product: Product) -> None:
        """Validate product can be added to cart."""
        if product.is_deleted:
            raise ProductInactiveException(detail="Product is no longer available")
        if not product.is_active:
            raise ProductInactiveException(detail="Product is inactive")

    @staticmethod
    def _validate_stock(product: Product, requested_total_qty: int) -> None:
        """Validate product has sufficient stock."""
        if requested_total_qty > product.stock_quantity:
            raise OutOfStockException(
                detail=f"Only {product.stock_quantity} items available in stock"
            )

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        """Validate quantity is positive."""
        if quantity <= 0:
            raise InvalidQuantityException(detail="Quantity must be greater than 0")

    @classmethod
    def calculate_totals(cls, cart: Cart) -> dict[str, Decimal]:
        """Calculate cart totals with tax and shipping."""
        subtotal = (
            cart.items.select_related("product")
            .aggregate(sum_subtotal=Sum(F("product__price") * F("quantity")))
            .get("sum_subtotal")
            or Decimal("0")
        )
        tax = subtotal * cls.TAX_RATE
        shipping = (
            Decimal("0")
            if subtotal > cls.SHIPPING_FREE_THRESHOLD
            else cls.SHIPPING_FEE
        )
        total = subtotal + tax + shipping
        return {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": total,
        }

    @staticmethod
    def add_item(cart: Cart, *, product_id: int, quantity: int) -> Cart:
        """Add (or increment) quantity for a product in cart."""
        CartService._validate_quantity(quantity)

        with transaction.atomic():
            product = (
                Product.objects.select_for_update()
                .select_related("category")
                .filter(id=product_id, is_deleted=False)
                .first()
            )

            if not product:
                raise ProductInactiveException(
                    detail="Product not found or is no longer available"
                )

            CartService._validate_product_for_cart(product)

            item, created = CartItem.objects.select_for_update().get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": 0},
            )
            new_qty = item.quantity + quantity
            CartService._validate_stock(product, new_qty)

            item.quantity = new_qty
            item.save(update_fields=["quantity"])
            return cart

    @staticmethod
    def update_quantity(cart: Cart, *, item_id: int, quantity: int) -> Cart:
        """Update quantity for a cart item."""
        CartService._validate_quantity(quantity)

        with transaction.atomic():
            item = (
                CartItem.objects.select_for_update()
                .select_related("product")
                .filter(id=item_id, cart=cart)
                .first()
            )

            if not item:
                raise ValueError("Cart item not found")

            product = item.product
            CartService._validate_product_for_cart(product)
            CartService._validate_stock(product, quantity)

            item.quantity = quantity
            item.save(update_fields=["quantity"])
            return cart

    @staticmethod
    def remove_item(cart: Cart, *, item_id: int) -> Cart:
        """Remove item from cart."""
        with transaction.atomic():
            CartItem.objects.filter(id=item_id, cart=cart).delete()
            return cart

    @staticmethod
    def clear_cart(cart: Cart) -> Cart:
        """Clear all items from cart."""
        with transaction.atomic():
            CartItem.objects.filter(cart=cart).delete()
            return cart

    @staticmethod
    def merge_cart(*, guest_cart: Cart, user_cart: Cart) -> Cart:
        """Merge guest cart into user cart and delete guest cart.
        
        Validates all products during merge and applies stock constraints.
        """
        if guest_cart.user_id is not None:
            raise ValueError("guest_cart must be a guest cart")
        if user_cart.user_id is None:
            raise ValueError("user_cart must be a user cart")

        with transaction.atomic():
            guest_items = (
                CartItem.objects.select_for_update()
                .select_related("product")
                .filter(cart=guest_cart)
            )

            for gi in guest_items:
                product = Product.objects.select_for_update().get(id=gi.product_id)
                CartService._validate_product_for_cart(product)

                user_item, _ = CartItem.objects.select_for_update().get_or_create(
                    cart=user_cart,
                    product=product,
                    defaults={"quantity": 0},
                )
                new_qty = user_item.quantity + gi.quantity
                CartService._validate_stock(product, new_qty)
                user_item.quantity = new_qty
                user_item.save(update_fields=["quantity"])

            CartItem.objects.filter(cart=guest_cart).delete()
            guest_cart.delete()

            return user_cart


