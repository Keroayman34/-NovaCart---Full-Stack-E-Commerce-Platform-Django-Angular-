from django.apps import apps
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from core.permissions import IsAdminUser


class CategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)


class AdminCategoryCreateView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategoryInputSerializer

    def post(self, request, *args, **kwargs):
        Category = apps.get_model("products", "Category")
        if Category is None:
            raise serializers.ValidationError("Category model not found.")

        incoming = request.data or {}
        writable_fields = {
            field.name
            for field in Category._meta.fields
            if field.name not in {"id", "pk", "created_at", "updated_at"}
        }

        payload = {key: value for key, value in incoming.items() if key in writable_fields}
        if not payload:
            raise serializers.ValidationError("No valid category fields provided.")

        category = Category.objects.create(**payload)
        return Response({"id": category.pk, **payload}, status=status.HTTP_201_CREATED)


class AdminCategoryDetailView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def _get_category(self, pk):
        Category = apps.get_model("products", "Category")
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise serializers.ValidationError("Category not found.")
        return category

    def put(self, request, *args, **kwargs):
        category = self._get_category(kwargs.get("pk"))
        incoming = request.data or {}

        writable_fields = {
            field.name
            for field in category._meta.fields
            if field.name not in {"id", "pk", "created_at", "updated_at"}
        }

        payload = {key: value for key, value in incoming.items() if key in writable_fields}
        if not payload:
            raise serializers.ValidationError("No valid category fields provided.")

        for key, value in payload.items():
            setattr(category, key, value)
        category.save(update_fields=list(payload.keys()))

        return Response({"id": category.pk, **payload}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        category = self._get_category(kwargs.get("pk"))
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminOrSellerOwnsProductPermission(permissions.BasePermission):
    message = "Only admin or the product owner can perform this action."

    def has_object_permission(self, request, view, obj):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False) or getattr(user, "role", None) == "admin":
            return True

        for owner_field in ("seller", "owner", "created_by", "user"):
            if hasattr(obj, owner_field) and getattr(obj, owner_field) == user:
                return True

        return False


class AdminProductSoftDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminOrSellerOwnsProductPermission]

    def _get_product(self, pk):
        Product = apps.get_model("products", "Product")
        product = Product.objects.filter(pk=pk).first()
        if not product:
            raise serializers.ValidationError("Product not found.")
        return product

    def delete(self, request, *args, **kwargs):
        product = self._get_product(kwargs.get("pk"))
        self.check_object_permissions(request, product)

        if hasattr(product, "is_deleted"):
            product.is_deleted = True
            product.save(update_fields=["is_deleted"])
        elif hasattr(product, "is_active"):
            product.is_active = False
            product.save(update_fields=["is_active"])
        elif hasattr(product, "status"):
            product.status = "deleted"
            product.save(update_fields=["status"])
        else:
            raise serializers.ValidationError("Soft-delete field is not available on Product model.")

        return Response(status=status.HTTP_204_NO_CONTENT)
