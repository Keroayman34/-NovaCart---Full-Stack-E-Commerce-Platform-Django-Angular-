from django.contrib.auth import get_user_model
from rest_framework import generics, serializers
from rest_framework.response import Response

from core.permissions import IsAdminUser


class AdminUserSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	username = serializers.CharField(read_only=True, allow_blank=True, required=False)
	first_name = serializers.CharField(read_only=True, allow_blank=True, required=False)
	last_name = serializers.CharField(read_only=True, allow_blank=True, required=False)
	email = serializers.EmailField(read_only=True, required=False)
	role = serializers.CharField(read_only=True, allow_blank=True, required=False)
	is_active = serializers.BooleanField(read_only=True)

	def to_representation(self, instance):
		return {
			"id": instance.pk,
			"username": getattr(instance, "username", ""),
			"first_name": getattr(instance, "first_name", ""),
			"last_name": getattr(instance, "last_name", ""),
			"email": getattr(instance, "email", ""),
			"role": getattr(instance, "role", ""),
			"is_active": getattr(instance, "is_active", True),
		}


class AdminUserUpdateSerializer(serializers.Serializer):
	is_active = serializers.BooleanField(required=False)
	role = serializers.CharField(required=False)

	def validate(self, attrs):
		if not attrs:
			raise serializers.ValidationError("Provide at least one field to update.")
		return attrs


class AdminUserListView(generics.ListAPIView):
	permission_classes = [IsAdminUser]
	serializer_class = AdminUserSerializer

	def get_queryset(self):
		User = get_user_model()
		queryset = User.objects.all().order_by("id")

		role = self.request.query_params.get("role")
		if role and hasattr(User, "role"):
			queryset = queryset.filter(role=role)

		status = self.request.query_params.get("status")
		if status == "active":
			queryset = queryset.filter(is_active=True)
		elif status in {"restricted", "inactive"}:
			queryset = queryset.filter(is_active=False)

		return queryset


class AdminUserUpdateView(generics.GenericAPIView):
	permission_classes = [IsAdminUser]
	serializer_class = AdminUserUpdateSerializer

	def get_queryset(self):
		return get_user_model().objects.all()

	def patch(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = self.get_queryset().filter(pk=kwargs.get("pk")).first()
		if not user:
			raise serializers.ValidationError("User not found.")

		update_fields = []
		if "is_active" in serializer.validated_data:
			user.is_active = serializer.validated_data["is_active"]
			update_fields.append("is_active")

		if "role" in serializer.validated_data and hasattr(user, "role"):
			user.role = serializer.validated_data["role"]
			update_fields.append("role")

		if update_fields:
			user.save(update_fields=update_fields)

		return Response(AdminUserSerializer(user).data)
