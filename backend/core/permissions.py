from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
	# allow admin users
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == "admin")


class IsSeller(BasePermission):
	# allow seller users
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == "seller")


class IsCustomer(BasePermission):
	# allow customer users
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == "customer")
