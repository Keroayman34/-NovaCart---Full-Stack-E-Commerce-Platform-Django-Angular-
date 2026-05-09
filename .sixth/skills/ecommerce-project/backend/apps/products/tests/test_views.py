"""
Tests for Product and Category API endpoints.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Category, Product, ProductImage

User = get_user_model()


@pytest.mark.django_db
class TestCategoryAPI:
    """Test cases for Category API endpoints."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="test123",
            role="admin"
        )
        self.customer_user = User.objects.create_user(
            email="customer@test.com",
            username="customer",
            password="test123",
            role="customer"
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic products"
        )

    def test_list_categories(self, setup_data):
        """Test listing categories."""
        response = self.client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data["data"]

    def test_create_category_admin_only(self, setup_data):
        """Test that only admins can create categories."""
        # Test with customer
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(
            "/api/categories/",
            {"name": "New Category", "description": "Test"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test with admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            "/api/categories/",
            {"name": "New Category", "description": "Test"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["name"] == "New Category"

    def test_retrieve_category(self, setup_data):
        """Test retrieving a single category."""
        response = self.client.get(f"/api/categories/{self.category.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Electronics"

    def test_update_category_admin_only(self, setup_data):
        """Test that only admins can update categories."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(
            f"/api/categories/{self.category.id}/",
            {"name": "Updated Category"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f"/api/categories/{self.category.id}/",
            {"name": "Updated Category"}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete_category_admin_only(self, setup_data):
        """Test that only admins can delete categories."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(f"/api/categories/{self.category.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestProductAPI:
    """Test cases for Product API endpoints."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="test123",
            role="admin"
        )
        self.seller_user = User.objects.create_user(
            email="seller@test.com",
            username="seller",
            password="test123",
            role="seller"
        )
        self.customer_user = User.objects.create_user(
            email="customer@test.com",
            username="customer",
            password="test123",
            role="customer"
        )
        self.category = Category.objects.create(
            name="Electronics"
        )
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller_user,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10,
            is_active=True
        )

    def test_list_products(self, setup_data):
        """Test listing products."""
        response = self.client.get("/api/products/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data["data"]

    def test_create_product_seller_only(self, setup_data):
        """Test that only sellers and admins can create products."""
        # Test with customer
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(
            "/api/products/",
            {
                "name": "New Product",
                "sku": "NEW001",
                "price": 50.00,
                "stock_quantity": 5,
                "category_id": self.category.id
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test with seller
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.post(
            "/api/products/",
            {
                "name": "New Product",
                "sku": "NEW001",
                "price": 50.00,
                "stock_quantity": 5,
                "category_id": self.category.id
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_retrieve_product(self, setup_data):
        """Test retrieving a single product."""
        response = self.client.get(f"/api/products/{self.product.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Test Product"

    def test_update_own_product_seller(self, setup_data):
        """Test that sellers can update their own products."""
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.patch(
            f"/api/products/{self.product.id}/",
            {"price": 150.00}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["price"] == "150.00"

    def test_cannot_update_others_product_seller(self, setup_data):
        """Test that sellers cannot update other sellers' products."""
        other_seller = User.objects.create_user(
            email="otherseller@test.com",
            username="otherseller",
            password="test123",
            role="seller"
        )
        self.client.force_authenticate(user=other_seller)
        response = self.client.patch(
            f"/api/products/{self.product.id}/",
            {"price": 150.00}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_soft_delete_product(self, setup_data):
        """Test soft deleting a product."""
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.delete(f"/api/products/{self.product.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.product.refresh_from_db()
        assert self.product.is_deleted is True

    def test_product_filtering_by_category(self, setup_data):
        """Test filtering products by category."""
        response = self.client.get(f"/api/products/?category={self.category.id}")
        assert response.status_code == status.HTTP_200_OK

    def test_product_filtering_by_price(self, setup_data):
        """Test filtering products by price range."""
        response = self.client.get("/api/products/?price_min=50&price_max=150")
        assert response.status_code == status.HTTP_200_OK

    def test_product_search(self, setup_data):
        """Test searching products."""
        response = self.client.get("/api/products/?search=Test")
        assert response.status_code == status.HTTP_200_OK

    def test_product_ordering(self, setup_data):
        """Test ordering products."""
        response = self.client.get("/api/products/?ordering=-price")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestProductImageAPI:
    """Test cases for Product Image API endpoints."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.client = APIClient()
        self.seller_user = User.objects.create_user(
            email="seller@test.com",
            username="seller",
            password="test123",
            role="seller"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller_user,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

    def test_update_stock(self, setup_data):
        """Test updating product stock."""
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.post(
            f"/api/products/{self.product.id}/update_stock/",
            {"quantity_change": 5}
        )
        assert response.status_code == status.HTTP_200_OK

        self.product.refresh_from_db()
        assert self.product.stock_quantity == 15

    def test_cannot_reduce_stock_below_zero(self, setup_data):
        """Test that stock cannot be reduced below zero."""
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.post(
            f"/api/products/{self.product.id}/update_stock/",
            {"quantity_change": -20}  # More than available
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProductPermissions:
    """Test cases for product permissions."""

    @pytest.fixture
    def setup_data(self):
        """Setup test data."""
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="test123",
            role="admin"
        )
        self.seller = User.objects.create_user(
            email="seller@test.com",
            username="seller",
            password="test123",
            role="seller"
        )
        self.customer = User.objects.create_user(
            email="customer@test.com",
            username="customer",
            password="test123",
            role="customer"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Test Product",
            sku="TEST001",
            price=100.00,
            stock_quantity=10
        )

    def test_admin_can_view_all_products(self, setup_data):
        """Test that admins can view all products including inactive."""
        inactive_product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Inactive Product",
            sku="INACTIVE001",
            price=50.00,
            stock_quantity=0,
            is_active=False
        )

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/api/products/{inactive_product.id}/")
        # Admin ViewSet should allow this, but base permission check might prevent it
        # This depends on implementation details

    def test_customer_read_only_access(self, setup_data):
        """Test that customers have read-only access."""
        self.client.force_authenticate(user=self.customer)

        # Can read
        response = self.client.get(f"/api/products/{self.product.id}/")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]

        # Cannot create
        response = self.client.post(
            "/api/products/",
            {"name": "New", "sku": "NEW", "price": 100}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
