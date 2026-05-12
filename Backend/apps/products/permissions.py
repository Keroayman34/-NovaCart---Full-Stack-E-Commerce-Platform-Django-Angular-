"""
Custom permission classes for product-related operations.
"""
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to allow admins full access, others read-only.
    """

    def has_permission(self, request, view):
        # Read operations are allowed to authenticated users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write operations only for admins
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsSellerOrAdmin(BasePermission):
    """
    Permission to allow sellers and admins to create products.
    Sellers can only edit/delete their own products.
    """

    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        # Allow sellers and admins to create
        if request.method in ["POST"]:
            return request.user.role in ["seller", "admin"]


        # Allow update/delete for sellers and admins
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user.role in ["seller", "admin"]

        return False

    def has_object_permission(self, request, view, obj):
        # Read operations allowed for all
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Admins can do anything
        if request.user.role == "admin":
            return True

        # Sellers can only modify their own products
        if request.user.role == "seller":
            return obj.seller_id == request.user.id

        return False


class IsCategoryAdmin(BasePermission):
    """
    Permission for category operations.
    - Customers: read-only
    - Sellers: read-only
    - Admins: full access
    """

    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        # Write operations only for admins
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsProductOwnerOrAdmin(BasePermission):
    """
    Permission to check if user is the product owner or admin.
    Used for product update/delete operations.
    """

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.role == "admin":
            return True

        # Product owners (sellers) can modify their products
        if request.user.role == "seller":
            return obj.seller_id == request.user.id

        return False


class IsReadOnlyCustomer(BasePermission):
    """
    Permission for customers to only read products and categories.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return bool(request.user and request.user.is_authenticated)

        return False
