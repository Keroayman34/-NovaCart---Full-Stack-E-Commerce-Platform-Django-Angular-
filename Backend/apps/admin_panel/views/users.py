from django.contrib.auth import get_user_model

from rest_framework import generics, serializers
from rest_framework.response import Response

from core.permissions import IsAdminUser

from apps.admin_panel.serializers import (
    AdminUserSerializer,
    AdminUserUpdateSerializer,
)

from apps.admin_panel.services import (
    UserManagementService,
)


class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        User = get_user_model()

        queryset = User.objects.filter(
            is_deleted=False
        ).order_by("id")

        role = self.request.query_params.get("role")

        if role:
            queryset = queryset.filter(role=role)

        status = self.request.query_params.get("status")

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class AdminUserUpdateView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserUpdateSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(
            is_deleted=False
        )

    def patch(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = self.get_queryset().filter(
            pk=kwargs.get("pk")
        ).first()

        if not user:
            raise serializers.ValidationError(
                "User not found."
            )

        update_fields = []

        if "is_active" in serializer.validated_data:
            user.is_active = serializer.validated_data[
                "is_active"
            ]

            update_fields.append(
                "is_active"
            )

        if "role" in serializer.validated_data:
            user.role = serializer.validated_data[
                "role"
            ]

            update_fields.append(
                "role"
            )

        if "status" in serializer.validated_data:

            status = serializer.validated_data[
                "status"
            ]

            if status == "approved":
                UserManagementService.approve_user(
                    user
                )

            elif status == "restricted":
                UserManagementService.restrict_user(
                    user
                )

            else:
                user.status = status
                update_fields.append(
                    "status"
                )

        if update_fields:
            user.save(
                update_fields=update_fields
            )

        return Response(
            AdminUserSerializer(
                user
            ).data
        )


class AdminUserDeleteView(
    generics.GenericAPIView
):
    permission_classes = [
        IsAdminUser
    ]

    def get_queryset(self):
        return get_user_model().objects.filter(
            is_deleted=False
        )

    def delete(
        self,
        request,
        *args,
        **kwargs
    ):

        user = self.get_queryset().filter(
            pk=kwargs.get("pk")
        ).first()

        if not user:
            raise serializers.ValidationError(
                "User not found."
            )

        UserManagementService.soft_delete(
            user
        )

        return Response(
            {
                "message":
                "User soft deleted successfully"
            }
        )