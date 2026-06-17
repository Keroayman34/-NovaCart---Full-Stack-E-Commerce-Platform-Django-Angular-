from django.apps import apps

from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status

from rest_framework.response import Response

from core.permissions import IsAdminUser


class CategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)


class AdminCategoryListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        Category = apps.get_model(
            "products",
            "Category"
        )

        queryset = Category.objects.all().order_by(
            "-created_at"
        )

        data = [
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
                "is_active": category.is_active,
            }
            for category in queryset
        ]

        return Response(data)


class AdminCategoryCreateView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategoryInputSerializer

    def post(self, request, *args, **kwargs):
        Category = apps.get_model(
            "products",
            "Category"
        )

        incoming = request.data or {}

        writable_fields = {
            field.name
            for field in Category._meta.fields
            if field.name not in {
                "id",
                "pk",
                "slug",
                "created_at",
                "updated_at",
            }
        }

        payload = {
            key: value
            for key, value in incoming.items()
            if key in writable_fields
        }

        if not payload:
            raise serializers.ValidationError(
                "No valid category fields provided."
            )

        category = Category(**payload)

        category.full_clean()
        category.save()

        return Response(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
                "is_active": category.is_active,
            },
            status=status.HTTP_201_CREATED
        )


class AdminCategoryDetailView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get_category(self, pk):
        Category = apps.get_model(
            "products",
            "Category"
        )

        category = Category.objects.filter(
            pk=pk
        ).first()

        if not category:
            raise serializers.ValidationError(
                "Category not found."
            )

        return category

    def patch(self, request, *args, **kwargs):
        category = self.get_category(
            kwargs.get("pk")
        )

        incoming = request.data or {}

        writable_fields = {
            field.name
            for field in category._meta.fields
            if field.name not in {
                "id",
                "pk",
                "slug",
                "created_at",
                "updated_at",
            }
        }

        payload = {
            key: value
            for key, value in incoming.items()
            if key in writable_fields
        }

        if not payload:
            raise serializers.ValidationError(
                "No valid category fields provided."
            )

        for key, value in payload.items():
            setattr(category, key, value)

        category.full_clean()

        category.save(
            update_fields=list(payload.keys())
        )

        return Response(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "description": category.description,
                "is_active": category.is_active,
            }
        )

    def delete(self, request, *args, **kwargs):
        category = self.get_category(
            kwargs.get("pk")
        )

        category.is_active = False

        category.save(
            update_fields=["is_active"]
        )

        return Response(
            {
                "message":
                "Category disabled successfully"
            }
        )


class AdminProductListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        Product = apps.get_model(
            "products",
            "Product"
        )

        queryset = Product.objects.filter(
            is_deleted=False
        ).select_related(
            "category",
            "seller"
        )

        data = [
            {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "price": str(product.price),
                "stock_quantity": product.stock_quantity,
                "category": product.category.name,
                "seller": product.seller.email,
                "is_active": product.is_active,
                "is_deleted": product.is_deleted,
            }
            for product in queryset
        ]

        return Response(data)


class AdminOrSellerOwnsProductPermission(
    permissions.BasePermission
):
    message = (
        "Only admin or the product owner "
        "can perform this action."
    )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        user = request.user

        if (
            user.is_staff
            or user.is_superuser
            or getattr(user, "role", None) == "admin"
        ):
            return True

        return obj.seller == user


class AdminProductSoftDeleteView(
    generics.GenericAPIView
):
    permission_classes = [
        permissions.IsAuthenticated,
        AdminOrSellerOwnsProductPermission,
    ]

    def get_product(self, pk):
        Product = apps.get_model(
            "products",
            "Product"
        )

        product = Product.objects.filter(
            pk=pk,
            is_deleted=False
        ).first()

        if not product:
            raise serializers.ValidationError(
                "Product not found."
            )

        return product

    def delete(self, request, *args, **kwargs):
        product = self.get_product(
            kwargs.get("pk")
        )

        self.check_object_permissions(
            request,
            product
        )

        product.soft_delete()

        return Response(
            {
                "message":
                "Product soft deleted successfully"
            }
        )