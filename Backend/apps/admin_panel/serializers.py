from rest_framework import serializers
from apps.orders.models import Order


class AdminUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        return {
            "id": instance.pk,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "role": instance.role,
            "is_active": instance.is_active,
            "status": instance.status,
            "is_deleted": instance.is_deleted,
        }


class AdminUserUpdateSerializer(serializers.Serializer):

    is_active = serializers.BooleanField(
        required=False
    )

    role = serializers.ChoiceField(
        choices=[
            "customer",
            "seller",
            "admin"
        ],
        required=False
    )

    status = serializers.ChoiceField(
        choices=[
            "pending",
            "approved",
            "restricted"
        ],
        required=False
    )

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "Provide at least one field to update."
            )

        return attrs
    

class AdminUpdateStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES,
        required=True
    )