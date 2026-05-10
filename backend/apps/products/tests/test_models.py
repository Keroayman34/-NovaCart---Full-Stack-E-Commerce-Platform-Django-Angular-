"""
Tests for Product and Category models.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..models import Category, Product, ProductImage

User = get_user_model()


@pytest.mark.django_db
class TestCategoryModel:
    """Test cases for Category model."""

    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name="Electronics",
            description="Electronic products"
        )
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.is_active is True

    def test_category_slug_auto_generation(self):
        """Test automatic slug generation from name."""
        category = Category.objects.create(
            name="Mobile Phones"
        )
        assert category.slug == "mobile-phones"

    def test_category_unique_name_validation(self):
        """Test that duplicate category names are rejected."""
        Category.objects.create(name="Phones")
        
        category2 = Category(name="Phones")
        with pytest.raises(ValidationError):
            category2.full_clean()

    def test_category_soft_delete(self):
        """Test soft deleting a category."""
        category = Category.objects.create(name="Laptops")
        assert category.is_active is True
        
        category.is_active = False
        category.save()
        
        assert Category.objects.filter(is_active=True).count() == 0

    def test_category_unique_slug(self):
        """Test that category slugs are unique."""
        Category.objects.create(name="Phones")
        
        with pytest.raises(IntegrityError):
            Category.objects.create(slug="phones", name="Other Phones")


@pytest.mark.django_db
class TestProductModel:
    """Test cases for Product model."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.category = Category.objects.create(name="Electronics")
        self.seller = User.objects.create_user(
            email="seller@test.com",
            username="seller",
            password="test123",
            role="seller"
        )

    def test_create_product(self, setup_data):
        """Test creating a product."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="iPhone 13",
            sku="IPHONE13",
            price=999.99,
            stock_quantity=10
        )
        assert product.name == "iPhone 13"
        assert product.slug == "iphone-13"
        assert product.price == 999.99
        assert product.is_in_stock is True

    def test_product_slug_auto_generation(self, setup_data):
        """Test automatic slug generation."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Samsung Galaxy S21",
            sku="SGS21",
            price=799.99,
            stock_quantity=5
        )
        assert product.slug == "samsung-galaxy-s21"

    def test_product_unique_sku(self, setup_data):
        """Test that SKU must be unique."""
        Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Product 1",
            sku="SKU001",
            price=100.00,
            stock_quantity=10
        )
        
        with pytest.raises(IntegrityError):
            Product.objects.create(
                category=self.category,
                seller=self.seller,
                name="Product 2",
                sku="SKU001",
                price=200.00,
                stock_quantity=5
            )

    def test_product_price_validation(self, setup_data):
        """Test price validation."""
        product = Product(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=0,  # Invalid price
            stock_quantity=10
        )
        
        with pytest.raises(ValidationError):
            product.full_clean()

    def test_product_stock_validation(self, setup_data):
        """Test stock quantity validation."""
        product = Product(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=-5  # Invalid stock
        )
        
        with pytest.raises(ValidationError):
            product.full_clean()

    def test_product_soft_delete(self, setup_data):
        """Test soft deleting a product."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )
        
        assert product.is_deleted is False
        product.soft_delete()
        
        product.refresh_from_db()
        assert product.is_deleted is True

    def test_product_restore(self, setup_data):
        """Test restoring a soft-deleted product."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10,
            is_deleted=True
        )
        
        product.restore()
        product.refresh_from_db()
        assert product.is_deleted is False

    def test_product_in_stock(self, setup_data):
        """Test in_stock property."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="In Stock Product",
            sku="INSTOCK",
            price=100.00,
            stock_quantity=5
        )
        assert product.is_in_stock is True
        
        product.stock_quantity = 0
        product.save()
        assert product.is_in_stock is False


@pytest.mark.django_db
class TestProductImageModel:
    """Test cases for ProductImage model."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.category = Category.objects.create(name="Electronics")
        self.seller = User.objects.create_user(
            email="seller@test.com",
            username="seller",
            password="test123",
            role="seller"
        )
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

    def test_create_product_image(self, setup_data):
        """Test creating a product image."""
        image = ProductImage.objects.create(
            product=self.product,
            image="test.jpg",
            is_primary=True,
            alt_text="Test image"
        )
        assert image.product == self.product
        assert image.is_primary is True

    def test_primary_image_uniqueness(self, setup_data):
        """Test that only one primary image per product is allowed."""
        ProductImage.objects.create(
            product=self.product,
            image="image1.jpg",
            is_primary=True
        )
        
        # This should unset the first image's primary flag
        image2 = ProductImage.objects.create(
            product=self.product,
            image="image2.jpg",
            is_primary=True
        )
        
        image1 = ProductImage.objects.get(image="image1.jpg")
        assert image1.is_primary is False
        assert image2.is_primary is True

    def test_multiple_images_per_product(self, setup_data):
        """Test that a product can have multiple images."""
        ProductImage.objects.create(
            product=self.product,
            image="image1.jpg"
        )
        ProductImage.objects.create(
            product=self.product,
            image="image2.jpg"
        )
        ProductImage.objects.create(
            product=self.product,
            image="image3.jpg"
        )
        
        assert self.product.images.count() == 3
