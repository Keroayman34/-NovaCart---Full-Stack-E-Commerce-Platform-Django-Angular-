"""
Tests for service layer.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import Category, Product, ProductImage
from ..services import (
    CategoryService,
    ProductService,
    ProductImageService,
)

User = get_user_model()


@pytest.mark.django_db
class TestCategoryService:
    """Test cases for CategoryService."""

    def test_create_category(self):
        """Test creating a category through service."""
        category = CategoryService.create_category(
            name="Electronics",
            description="Electronic products"
        )
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.is_active is True

    def test_update_category(self):
        """Test updating a category through service."""
        category = Category.objects.create(name="Phones")
        updated = CategoryService.update_category(
            category,
            description="Mobile phones",
            name="Mobile Phones"
        )
        assert updated.name == "Mobile Phones"
        assert updated.description == "Mobile phones"

    def test_delete_category(self):
        """Test soft deleting a category through service."""
        category = Category.objects.create(name="Phones")
        CategoryService.delete_category(category)
        
        category.refresh_from_db()
        assert category.is_active is False

    def test_activate_category(self):
        """Test activating a category through service."""
        category = Category.objects.create(name="Phones", is_active=False)
        CategoryService.activate_category(category)
        
        category.refresh_from_db()
        assert category.is_active is True


@pytest.mark.django_db
class TestProductService:
    """Test cases for ProductService."""

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

    def test_generate_slug_unique(self, setup_data):
        """Test slug generation with uniqueness."""
        slug1 = ProductService.generate_slug("iPhone 13")
        slug2 = ProductService.generate_slug("iPhone 13")
        assert slug1 != slug2
        assert slug1 == "iphone-13"
        assert slug2 == "iphone-13-1"

    def test_create_product(self, setup_data):
        """Test creating a product through service."""
        product = ProductService.create_product(
            category=self.category,
            seller=self.seller,
            name="iPhone 13",
            sku="IPHONE13",
            price=999.99,
            stock_quantity=10
        )
        assert product.name == "iPhone 13"
        assert product.price == 999.99
        assert product.stock_quantity == 10

    def test_create_product_invalid_price(self, setup_data):
        """Test creating product with invalid price."""
        with pytest.raises(ValidationError):
            ProductService.create_product(
                category=self.category,
                seller=self.seller,
                name="Test",
                sku="TEST",
                price=-10,
                stock_quantity=10
            )

    def test_update_product(self, setup_data):
        """Test updating a product through service."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

        updated = ProductService.update_product(
            product,
            price=150.00,
            stock_quantity=20
        )
        assert updated.price == 150.00
        assert updated.stock_quantity == 20

    def test_soft_delete_product(self, setup_data):
        """Test soft deleting a product through service."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

        ProductService.soft_delete_product(product)
        product.refresh_from_db()
        assert product.is_deleted is True

    def test_restore_product(self, setup_data):
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

        ProductService.restore_product(product)
        product.refresh_from_db()
        assert product.is_deleted is False

    def test_update_stock_increase(self, setup_data):
        """Test increasing stock."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

        ProductService.update_stock(product, 5)
        product.refresh_from_db()
        assert product.stock_quantity == 15

    def test_update_stock_decrease(self, setup_data):
        """Test decreasing stock."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

        ProductService.update_stock(product, -3)
        product.refresh_from_db()
        assert product.stock_quantity == 7

    def test_update_stock_negative(self, setup_data):
        """Test that stock cannot go negative."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=5
        )

        with pytest.raises(ValidationError):
            ProductService.update_stock(product, -10)

    def test_deactivate_product(self, setup_data):
        """Test deactivating a product."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

        ProductService.deactivate_product(product)
        product.refresh_from_db()
        assert product.is_active is False

    def test_activate_product(self, setup_data):
        """Test activating a product."""
        product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10,
            is_active=False
        )

        ProductService.activate_product(product)
        product.refresh_from_db()
        assert product.is_active is True


@pytest.mark.django_db
class TestProductImageService:
    """Test cases for ProductImageService."""

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

    def test_add_image(self, setup_data):
        """Test adding an image to a product."""
        image = ProductImageService.add_image(
            product=self.product,
            image="test.jpg",
            is_primary=True,
            alt_text="Test image"
        )
        assert image.product == self.product
        assert image.is_primary is True

    def test_remove_image(self, setup_data):
        """Test removing an image."""
        image = ProductImage.objects.create(
            product=self.product,
            image="test.jpg"
        )
        ProductImageService.remove_image(image)
        
        with pytest.raises(ProductImage.DoesNotExist):
            ProductImage.objects.get(pk=image.pk)

    def test_set_primary_image(self, setup_data):
        """Test setting a primary image."""
        image1 = ProductImage.objects.create(
            product=self.product,
            image="image1.jpg",
            is_primary=True
        )
        image2 = ProductImage.objects.create(
            product=self.product,
            image="image2.jpg"
        )

        ProductImageService.set_primary_image(self.product, image2)
        
        image1.refresh_from_db()
        image2.refresh_from_db()
        assert image1.is_primary is False
        assert image2.is_primary is True

    def test_get_primary_image(self, setup_data):
        """Test getting the primary image."""
        image1 = ProductImage.objects.create(
            product=self.product,
            image="image1.jpg"
        )
        image2 = ProductImage.objects.create(
            product=self.product,
            image="image2.jpg",
            is_primary=True
        )

        primary = ProductImageService.get_primary_image(self.product)
        assert primary == image2
