"""Cart API views for NovaCart."""

from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from apps.products.models import Product
from core.utils import api_response
from core.exceptions import CartException, CartOwnershipException

from .models import Cart, CartItem
from .permissions import IsCartOwner, IsCartItemOwner
from .serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)
from .services import CartService
from .throttles import CartUserThrottle, CartAnonThrottle


class CartViewSet(viewsets.ViewSet):
    """Cart endpoints."""

    permission_classes = []
    throttle_classes = [CartUserThrottle, CartAnonThrottle]

    def _get_request_cart(self) -> Cart:
        return CartService.get_or_create_cart(self.request)

    def list(self, request):
        cart = self._get_request_cart()
        cart = (
            Cart.objects.select_related("user")
            .prefetch_related("items__product")
            .get(id=cart.id)
        )

        if not self._is_cart_owner(cart):
            raise CartOwnershipException()

        serializer = CartSerializer(cart)
        return api_response(
            success=True,
            data=serializer.data,
        )

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart = self._get_request_cart()

        if not self._is_cart_owner(cart):
            raise CartOwnershipException()

        CartService.clear_cart(cart)
        return api_response(success=True, data={})

    def _is_cart_owner(self, cart: Cart) -> bool:
        """Check if request user/session owns cart."""
        if self.request.user and self.request.user.is_authenticated:
            return cart.user_id == self.request.user.id

        session_key = self.request.session.session_key
        return bool(session_key) and cart.session_key == session_key


class CartItemViewSet(viewsets.ViewSet):
    """Cart item endpoints."""

    throttle_classes = [CartUserThrottle, CartAnonThrottle]

    def _get_request_cart(self) -> Cart:
        return CartService.get_or_create_cart(self.request)

    def _is_item_owner(self, item: CartItem) -> bool:
        """Check if request user/session owns cart item."""
        if self.request.user and self.request.user.is_authenticated:
            return item.cart.user_id == self.request.user.id

        session_key = self.request.session.session_key
        return bool(session_key) and item.cart.session_key == session_key

    def _get_fresh_cart(self, cart: Cart) -> Cart:
        """Retrieve cart with optimized queries."""
        return (
            Cart.objects.prefetch_related("items__product")
            .select_related("user")
            .get(id=cart.id)
        )

    def create(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self._get_request_cart()

        try:
            CartService.add_item(
                cart,
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )
        except CartException as e:
            return api_response(
                success=False,
                message=str(e.detail),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        cart = self._get_fresh_cart(cart)
        cart_serializer = CartSerializer(cart)
        return api_response(
            success=True,
            data=cart_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        item_id = int(pk)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self._get_request_cart()

        try:
            item = CartItem.objects.select_related("cart").get(
                id=item_id,
                cart=cart,
            )
            if not self._is_item_owner(item):
                raise CartOwnershipException()

            CartService.update_quantity(
                cart,
                item_id=item_id,
                quantity=serializer.validated_data["quantity"],
            )
        except CartItem.DoesNotExist:
            return api_response(
                success=False,
                message="Cart item not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except CartException as e:
            return api_response(
                success=False,
                message=str(e.detail),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        cart = self._get_fresh_cart(cart)
        return api_response(
            success=True,
            data=CartSerializer(cart).data,
        )

    def destroy(self, request, pk=None):
        item_id = int(pk)
        cart = self._get_request_cart()

        try:
            item = CartItem.objects.select_related("cart").get(
                id=item_id,
                cart=cart,
            )
            if not self._is_item_owner(item):
                raise CartOwnershipException()

            CartService.remove_item(cart, item_id=item_id)
        except CartItem.DoesNotExist:
            return api_response(
                success=False,
                message="Cart item not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return api_response(success=True, data={})


