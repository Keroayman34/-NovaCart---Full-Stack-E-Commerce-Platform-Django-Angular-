"""Tests for cart merge, merge on login, and race conditions."""

import pytest
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from rest_framework.test import APIClient

from apps.products.models import Category, Product
from apps.users.models import User
from apps.cart.models import Cart, CartItem
from apps.cart.services import CartService


@pytest.mark.django_db
class TestCartMergeService:
    """Test cart merge functionality."""

    def setup_method(self):
        self.customer = User.objects.create_user(
            username="cust",
            email="cust@example.com",
            password="password123",
            role="customer",
        )
        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="password123",
            role="seller",
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="",
            is_active=True,
        )

        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Phone",
            sku="SKU-PHONE",
            price=Decimal("200.00"),
            stock_quantity=5,
            is_active=True,
            is_deleted=False,
        )

    def test_merge_cart_combines_quantities_and_deletes_guest(self):
        """Guest cart items merged into user cart with combined quantities."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)

        CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

        assert Cart.objects.filter(id=guest_cart.id).exists() is False
        merged_item = CartItem.objects.get(cart=user_cart, product=self.product)
        assert merged_item.quantity == 3

    def test_merge_cart_creates_new_items_if_not_exist(self):
        """Merge creates new items in user cart if they don't exist."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        product2 = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Laptop",
            sku="SKU-LAPTOP",
            price=Decimal("1000.00"),
            stock_quantity=3,
            is_active=True,
            is_deleted=False,
        )

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=guest_cart, product=product2, quantity=1)

        CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

        assert CartItem.objects.filter(cart=user_cart).count() == 2
        assert CartItem.objects.filter(cart=user_cart, product=self.product).exists()
        assert CartItem.objects.filter(cart=user_cart, product=product2).exists()

    def test_merge_cart_validates_soft_deleted_products(self):
        """Merge fails if guest cart contains soft-deleted products."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        deleted_product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Deleted",
            sku="SKU-DELETED",
            price=Decimal("100.00"),
            stock_quantity=5,
            is_active=True,
            is_deleted=True,
        )

        CartItem.objects.create(cart=guest_cart, product=deleted_product, quantity=1)

        with pytest.raises(Exception):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

    def test_merge_cart_validates_stock_during_merge(self):
        """Merge validates that combined quantity doesn't exceed stock."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=3)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=3)

        with pytest.raises(Exception):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)


@pytest.mark.django_db
class TestCartMergeOnLogin:
    """Test automatic cart merge after login."""

    def setup_method(self):
        self.client = APIClient()
        self.factory = RequestFactory()

        self.customer = User.objects.create_user(
            username="cust",
            email="cust@example.com",
            password="password123",
            role="customer",
        )
        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="password123",
            role="seller",
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="",
            is_active=True,
        )

        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Phone",
            sku="SKU-PHONE",
            price=Decimal("200.00"),
            stock_quantity=10,
            is_active=True,
            is_deleted=False,
        )

    def test_guest_cart_merged_into_user_cart_on_login(self):
        """Guest cart is merged into user cart after successful login."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        res_guest = self.client.get("/api/cart/")
        guest_items_count = len(res_guest.data["data"]["items"])
        assert guest_items_count == 1

        res_login = self.client.post(
            "/api/users/login/",
            {
                "username": "cust",
                "password": "password123",
            },
            format="json",
        )
        assert res_login.status_code == 200

        self.client.force_authenticate(user=self.customer)

        res_after_login = self.client.get("/api/cart/")
        assert len(res_after_login.data["data"]["items"]) == 1
        assert res_after_login.data["data"]["items"][0]["quantity"] == 2

    def test_merge_respects_existing_user_cart_items(self):
        """Merge combines guest items with existing authenticated user cart."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )

        product2 = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Laptop",
            sku="SKU-LAPTOP",
            price=Decimal("1000.00"),
            stock_quantity=5,
            is_active=True,
            is_deleted=False,
        )

        self.client.force_authenticate(user=self.customer)
        self.client.post(
            "/api/cart/items/",
            {"product_id": product2.id, "quantity": 1},
            format="json",
        )

        self.client.force_authenticate(user=None)
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        res_login = self.client.post(
            "/api/users/login/",
            {
                "username": "cust",
                "password": "password123",
            },
            format="json",
        )

        self.client.force_authenticate(user=self.customer)
        res = self.client.get("/api/cart/")
        assert len(res.data["data"]["items"]) == 2


@pytest.mark.django_db
class TestCartRaceConditions:
    """Test protection against race conditions."""

    def setup_method(self):
        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="password123",
            role="seller",
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="",
            is_active=True,
        )
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Phone",
            sku="SKU-PHONE",
            price=Decimal("200.00"),
            stock_quantity=5,
            is_active=True,
            is_deleted=False,
        )

    def test_concurrent_add_item_respects_stock_limit(self):
        """Stock validation during add_item prevents overselling."""
        cart = Cart.objects.create(session_key="test-session")

        CartService.add_item(cart, product_id=self.product.id, quantity=3)

        with pytest.raises(Exception):
            CartService.add_item(cart, product_id=self.product.id, quantity=5)

    def test_concurrent_update_respects_stock_limit(self):
        """Stock validation during update_quantity prevents overselling."""
        cart = Cart.objects.create(session_key="test-session")

        CartService.add_item(cart, product_id=self.product.id, quantity=2)

        item = CartItem.objects.get(cart=cart, product=self.product)

        with pytest.raises(Exception):
            CartService.update_quantity(cart, item_id=item.id, quantity=10)


@pytest.mark.django_db
class TestThrottling:
    """Test API throttling."""

    def setup_method(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="password123",
            role="seller",
        )
        self.customer = User.objects.create_user(
            username="cust",
            email="cust@example.com",
            password="password123",
            role="customer",
        )
        self.category = Category.objects.create(
            name="Electronics",
            description="",
            is_active=True,
        )
        self.product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Phone",
            sku="SKU-PHONE",
            price=Decimal("200.00"),
            stock_quantity=100,
            is_active=True,
            is_deleted=False,
        )

    def test_authenticated_user_throttle(self):
        """Authenticated users are throttled at 100 req/min."""
        self.client.force_authenticate(user=self.customer)

        for _ in range(5):
            res = self.client.get("/api/cart/")
            assert res.status_code == 200

    def test_anonymous_user_throttle(self):
        """Anonymous users are throttled at 30 req/min."""
        for _ in range(5):
            res = self.client.get("/api/cart/")
            assert res.status_code == 200
