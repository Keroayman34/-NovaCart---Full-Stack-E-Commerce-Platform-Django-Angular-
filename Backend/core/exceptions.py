"""Custom exceptions and DRF exception handlers."""

from __future__ import annotations

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CartException(APIException):
    """Base exception for cart operations."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Cart operation failed"
    default_code = "cart_error"


class OutOfStockException(CartException):
    """Product is out of stock."""

    default_detail = "Out of stock"
    default_code = "out_of_stock"


class InvalidQuantityException(CartException):
    """Invalid quantity provided."""

    default_detail = "Invalid quantity"
    default_code = "invalid_quantity"


class ProductInactiveException(CartException):
    """Product is no longer available or inactive."""

    default_detail = "Product is no longer available"
    default_code = "product_inactive"


class CartOwnershipException(APIException):
    """User does not own this cart."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to access this cart"
    default_code = "cart_ownership_denied"


def cart_exception_handler(exc: Exception, context: dict) -> Response | None:
    """Custom exception handler for cart API errors.
    
    Standardizes error responses to include success flag and message.
    Falls back to default DRF handler for non-cart exceptions.
    """
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, (CartException, CartOwnershipException)):
        return Response(
            {
                "success": False,
                "message": exc.detail if hasattr(exc, "detail") else str(exc),
            },
            status=response.status_code,
        )

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        errors = response.data
        if isinstance(errors, dict):
            error_msg = next(
                (str(v[0]) if isinstance(v, list) else str(v) for v in errors.values()),
                "Validation error",
            )
        else:
            error_msg = str(errors)

        return Response(
            {
                "success": False,
                "message": error_msg,
            },
            status=response.status_code,
        )

    return response
