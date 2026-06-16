from rest_framework import generics, status
from rest_framework.response import Response

from core.permissions import IsAdminUser

from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductSerializer
from .services import ProductService


class AdminCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by("-created_at")
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class AdminProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductDetailSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = (
            Product.objects.select_related("category", "seller")
            .prefetch_related("images")
            .filter(is_deleted=False)
            .order_by("-created_at")
        )
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(sku__icontains=search)
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save()


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductDetailSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.select_related("category", "seller").prefetch_related("images").filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        ProductService.soft_delete_product(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminProductSoftDeleteView(AdminProductDetailView):
    pass
