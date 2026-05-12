"""
Serializers for Product and Category models.
"""
from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    
    Provides full CRUD operations for categories.
    """
    url = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "products_count",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at", "url"]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
            }
        }

    def get_url(self, obj):
        """Get the category detail URL."""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/categories/{obj.slug}/")
        return f"/api/categories/{obj.slug}/"

    def get_products_count(self, obj):
        """Get the count of active products in the category."""
        return obj.products.filter(is_active=True, is_deleted=False).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    
    Handles image upload and validation.
    """
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_primary",
            "alt_text",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for listing products.
    
    Used for list views to reduce payload size.
    Includes only essential fields and primary image.
    """
    category_name = serializers.CharField(source="category.name", read_only=True)
    seller_name = serializers.CharField(source="seller.email", read_only=True)
    primary_image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "price",
            "stock_quantity",
            "is_in_stock",
            "category_name",
            "seller_name",
            "primary_image",
            "is_active",
            "url",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "is_in_stock",
            "created_at",
            "url",
        ]

    def get_primary_image(self, obj):
        """Get the primary image URL."""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

    def get_url(self, obj):
        """Get the product detail URL."""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/products/{obj.slug}/")
        return f"/api/products/{obj.slug}/"


class ProductSerializer(serializers.ModelSerializer):
    """
    Full serializer for Product model.
    
    Provides complete product data including nested images and category.
    Used for detail views and creation/update operations.
    """
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source="category",
        write_only=True,
    )
    seller_name = serializers.CharField(source="seller.email", read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__("django.contrib.auth", fromlist=["get_user_model"]).get_user_model().objects.none(),  # Will be updated in __init__
        source="seller",
        write_only=True,
        required=False,
    )
    images = ProductImageSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    is_owned_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "sku",
            "price",
            "stock_quantity",
            "is_in_stock",
            "is_active",
            "category_id",
            "category_name",
            "seller_id",
            "seller_name",
            "images",
            "is_owned_by_user",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "is_in_stock",
            "category_name",
            "seller_name",
            "is_owned_by_user",
            "url",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
            },
            "sku": {
                "required": True,
                "allow_blank": False,
            },
            "price": {
                "required": True,
                "min_value": 0.01,
            },
            "stock_quantity": {
                "required": True,
                "min_value": 0,
            },
        }

    def __init__(self, *args, **kwargs):
        """Initialize serializer and set seller queryset."""
        super().__init__(*args, **kwargs)
        # Allow sellers to be selected (only for admin/staff)
        self.fields["seller_id"].queryset = (
            __import__("django.contrib.auth", fromlist=["get_user_model"])
            .get_user_model()
            .objects.filter(role="seller")
        )

    def get_url(self, obj):
        """Get the product detail URL."""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/products/{obj.slug}/")
        return f"/api/products/{obj.slug}/"

    def get_is_owned_by_user(self, obj):
        """Check if the product is owned by the current user."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.seller_id == request.user.id
        return False

    def create(self, validated_data):
        """Create a new product."""
        # If seller is not provided, use the current user
        if "seller" not in validated_data:
            request = self.context.get("request")
            if request and request.user.is_authenticated:
                validated_data["seller"] = request.user
        
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        """Update a product."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProductDetailSerializer(ProductSerializer):
    """
    Extended serializer for product detail view.
    
    Includes additional related data and full image information.
    """
    category = CategorySerializer(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields.copy()
        # Replace category_id and category_name with full category object
        fields[fields.index("category_id")] = "category"
        read_only_fields = list(ProductSerializer.Meta.read_only_fields)
        read_only_fields.append("category")
