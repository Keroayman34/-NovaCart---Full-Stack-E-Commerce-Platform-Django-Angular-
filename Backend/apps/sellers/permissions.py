from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "seller"
            and hasattr(request.user, "seller_profile")
        )


class IsApprovedSeller(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role != "seller":
            return False
        try:
            return request.user.seller_profile.approval_status == "approved"
        except AttributeError:
            return False


class IsSellerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
