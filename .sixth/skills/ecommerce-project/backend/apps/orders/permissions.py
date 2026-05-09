from rest_framework.permissions import BasePermission


def _get_order_owner(order_item):
	product = getattr(order_item, "product", None)
	if product is None:
		return None

	for attribute_name in ("seller", "owner", "created_by", "user"):
		owner = getattr(product, attribute_name, None)
		if owner is not None:
			return owner

	return None


class CanUpdateOrderStatus(BasePermission):
	message = "You do not have permission to update this order status."

	def has_object_permission(self, request, view, obj):
		user = getattr(request, "user", None)
		if not user or not user.is_authenticated:
			return False

		if user.is_staff or user.is_superuser:
			return True

		for order_item in obj.items.select_related("product"):
			owner = _get_order_owner(order_item)
			if owner == user:
				return True

		return False