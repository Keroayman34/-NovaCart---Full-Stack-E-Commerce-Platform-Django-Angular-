"""
ViewSets for Product and Category operations.
"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import models

from core.pagination import CustomPagination
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsSellerOrAdmin,
    IsCategoryAdmin,
    IsProductOwnerOrAdmin,
)
from .filters import (
    CategoryFilter,
    ProductFilter,
    ProductSearchFilter,
    ProductOrderingFilter,
)
from .services import (
    CategoryService,
    ProductService,
    ProductImageService,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations.
    
    Endpoints:
        - GET /api/categories/ - List all active categories
        - GET /api/categories/{id}/ - Get category by ID
        - GET /api/categories/slug/{slug}/ - Get category by slug
        - POST /api/categories/ - Create category (admin only)
        - PATCH /api/categories/{id}/ - Update category (admin only)
        - DELETE /api/categories/{id}/ - Delete category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsCategoryAdmin]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryFilter
    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Filter queryset based on user role.
        - Customers/Sellers: Only active categories
        - Admins: All categories
        """
        queryset = Category.objects.all()
        
        if self.request.user.is_authenticated:
            if self.request.user.role != "admin":
                queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by("-created_at")

    @action(detail=False, methods=["get"])
    def by_slug(self, request, slug=None):
        """
        Get category by slug.
        
        Example: GET /api/categories/by_slug/?slug=electronics
        """
        slug = request.query_params.get("slug")
        if not slug:
            return Response(
                {"success": False, "message": "Slug parameter required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        category = get_object_or_404(Category, slug=slug, is_active=True)
        serializer = self.get_serializer(category)
        return Response({"success": True, "data": serializer.data})

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Activate a category (admin only)."""
        if request.user.role != "admin":
            return Response(
                {"success": False, "message": "Only admins can activate categories"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        category = self.get_object()
        CategoryService.activate_category(category)
        serializer = self.get_serializer(category)
        return Response({"success": True, "data": serializer.data})

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """Deactivate a category (admin only)."""
        if request.user.role != "admin":
            return Response(
                {"success": False, "message": "Only admins can deactivate categories"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        category = self.get_object()
        CategoryService.delete_category(category)
        serializer = self.get_serializer(category)
        return Response({"success": True, "data": serializer.data})

    def create(self, request, *args, **kwargs):
        """Create a new category (admin only)."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            category = CategoryService.create_category(
                name=serializer.validated_data.get("name"),
                description=serializer.validated_data.get("description"),
                image=serializer.validated_data.get("image"),
            )
            serializer = self.get_serializer(category)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        """Update a category (admin only)."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            category = CategoryService.update_category(instance, **serializer.validated_data)
            serializer = self.get_serializer(category)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations.
    
    Endpoints:
        - GET /api/products/ - List products with filtering
        - GET /api/products/{id}/ - Get product by ID
        - GET /api/products/slug/{slug}/ - Get product by slug
        - POST /api/products/ - Create product (seller/admin only)
        - PATCH /api/products/{id}/ - Update product (owner/admin only)
        - DELETE /api/products/{id}/ - Delete product (owner/admin only)
        - POST /api/products/{id}/upload_image/ - Upload product image
        - POST /api/products/{id}/set_primary_image/ - Set primary image
    """
    queryset = Product.objects.filter(is_deleted=False, is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrAdmin]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        ProductSearchFilter,
        ProductOrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "sku"]
    ordering_fields = ["price", "created_at", "name", "stock_quantity"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Optimize queries and filter based on user role.
        
        - Customers/Anonymous: Only active, non-deleted products
        - Sellers: Their own products + active products
        - Admins: All products
        """
        queryset = Product.objects.select_related(
            "category",
            "seller"
        ).prefetch_related("images").filter(is_deleted=False)
        
        if not self.request.user.is_authenticated:
            # Anonymous users: only active products
            queryset = queryset.filter(is_active=True)
        elif self.request.user.role == "seller":
            # Sellers: their own products + active products
            queryset = queryset.filter(
                models.Q(seller=self.request.user) | models.Q(is_active=True)
            )
        # Admins see all (not deleted) products
        
        return queryset.order_by("-created_at")

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "retrieve":
            return ProductDetailSerializer
        elif self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False, methods=["get"])
    def by_slug(self, request, slug=None):
        """
        Get product by slug.
        
        Example: GET /api/products/by_slug/?slug=iphone-13-pro
        """
        slug = request.query_params.get("slug")
        if not slug:
            return Response(
                {"success": False, "message": "Slug parameter required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        product = get_object_or_404(
            Product,
            slug=slug,
            is_deleted=False,
            is_active=True,
        )
        serializer = ProductDetailSerializer(product, context={"request": request})
        return Response({"success": True, "data": serializer.data})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def upload_image(self, request, pk=None):
        """
        Upload an image for the product.
        
        Required fields:
            - image: Image file
            - is_primary (optional): Set as primary image
            - alt_text (optional): Alternative text
        """
        product = self.get_object()
        
        # Check if user owns the product or is admin
        if product.seller_id != request.user.id and request.user.role != "admin":
            return Response(
                {"success": False, "message": "You can only upload images for your own products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            image = ProductImageService.add_image(
                product=product,
                image=serializer.validated_data.get("image"),
                is_primary=serializer.validated_data.get("is_primary", False),
                alt_text=serializer.validated_data.get("alt_text"),
            )
            serializer = ProductImageSerializer(image)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def set_primary_image(self, request, pk=None):
        """
        Set a product image as primary.
        
        Required fields:
            - image_id: ID of the image to set as primary
        """
        product = self.get_object()
        
        # Check if user owns the product or is admin
        if product.seller_id != request.user.id and request.user.role != "admin":
            return Response(
                {"success": False, "message": "You can only modify your own products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        image_id = request.data.get("image_id")
        if not image_id:
            return Response(
                {"success": False, "message": "image_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            image = ProductImage.objects.get(id=image_id, product=product)
            ProductImageService.set_primary_image(product, image)
            return Response(
                {
                    "success": True,
                    "message": "Primary image set successfully",
                    "data": ProductImageSerializer(image).data,
                }
            )
        except ProductImage.DoesNotExist:
            return Response(
                {"success": False, "message": "Image not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def delete_image(self, request, pk=None):
        """
        Delete a product image.
        
        Required fields:
            - image_id: ID of the image to delete
        """
        product = self.get_object()
        
        # Check if user owns the product or is admin
        if product.seller_id != request.user.id and request.user.role != "admin":
            return Response(
                {"success": False, "message": "You can only modify your own products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        image_id = request.data.get("image_id")
        if not image_id:
            return Response(
                {"success": False, "message": "image_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            image = ProductImage.objects.get(id=image_id, product=product)
            ProductImageService.remove_image(image)
            return Response(
                {"success": True, "message": "Image deleted successfully"}
            )
        except ProductImage.DoesNotExist:
            return Response(
                {"success": False, "message": "Image not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def update_stock(self, request, pk=None):
        """
        Update product stock quantity.
        
        Required fields:
            - quantity_change: Amount to change stock by (positive/negative)
        """
        product = self.get_object()
        
        # Check if user owns the product or is admin
        if product.seller_id != request.user.id and request.user.role != "admin":
            return Response(
                {"success": False, "message": "You can only modify your own products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        quantity_change = request.data.get("quantity_change")
        if quantity_change is None:
            return Response(
                {"success": False, "message": "quantity_change is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            ProductService.update_stock(product, int(quantity_change))
            serializer = ProductDetailSerializer(product, context={"request": request})
            return Response(
                {"success": True, "data": serializer.data}
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        """Restore a soft-deleted product (admin only)."""
        if request.user.role != "admin":
            return Response(
                {"success": False, "message": "Only admins can restore products"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        product = Product.objects.get(pk=pk)
        if not product.is_deleted:
            return Response(
                {"success": False, "message": "Product is not deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        ProductService.restore_product(product)
        serializer = ProductDetailSerializer(product, context={"request": request})
        return Response({"success": True, "data": serializer.data})

    def create(self, request, *args, **kwargs):
        """Create a new product."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Use current user as seller if not specified and user is seller
            seller = serializer.validated_data.get("seller", request.user)
            
            product = ProductService.create_product(
                category=serializer.validated_data.get("category"),
                seller=seller,
                name=serializer.validated_data.get("name"),
                sku=serializer.validated_data.get("sku"),
                price=serializer.validated_data.get("price"),
                stock_quantity=serializer.validated_data.get("stock_quantity"),
                description=serializer.validated_data.get("description"),
                is_active=serializer.validated_data.get("is_active", True),
            )
            serializer = ProductDetailSerializer(product, context={"request": request})
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        """Update a product."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            product = ProductService.update_product(
                instance,
                **serializer.validated_data
            )
            serializer = ProductDetailSerializer(product, context={"request": request})
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        """Soft delete a product."""
        instance = self.get_object()
        ProductService.soft_delete_product(instance)
        return Response(
            {"success": True, "message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
