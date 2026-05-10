"""Permissions for cart APIs."""

from __future__ import annotations

from rest_framework.permissions import BasePermission

from .models import Cart, CartItem


class IsCartOwner(BasePermission):
    """Ensure the cart belongs to the requesting user/session."""

    def has_object_permission(self, request, view, obj: Cart) -> bool:
        if request.user and request.user.is_authenticated:
            return obj.user_id == request.user.id

        session_key = request.session.session_key
        return bool(session_key) and obj.session_key == session_key


class IsCartItemOwner(BasePermission):
    """Ensure the cart item belongs to the requesting user/session."""

    def has_object_permission(self, request, view, obj: CartItem) -> bool:
        if request.user and request.user.is_authenticated:
            return obj.cart.user_id == request.user.id

        session_key = request.session.session_key
        return bool(session_key) and obj.cart.session_key == session_key

