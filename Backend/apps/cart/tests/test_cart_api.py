import pytest
from decimal import Decimal
from rest_framework.test import APIClient

from apps.products.models import Category, Product
from apps.users.models import User
from apps.cart.models import Cart, CartItem


@pytest.mark.django_db
class TestCartAPI:
    def setup_method(self):
        self.client = APIClient()

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
        
        self.product_inactive = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Inactive Product",
            sku="SKU-INACTIVE",
            price=Decimal("100.00"),
            stock_quantity=10,
            is_active=False,
            is_deleted=False,
        )
        
        self.product_deleted = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Deleted Product",
            sku="SKU-DELETED",
            price=Decimal("150.00"),
            stock_quantity=10,
            is_active=True,
            is_deleted=True,
        )

    def test_guest_cart_create_and_add_item(self):
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        assert res.status_code in (200, 201)
        assert res.data["success"] is True

        res2 = self.client.get("/api/cart/")
        assert res2.status_code == 200
        assert res2.data["success"] is True
        assert len(res2.data["data"]["items"]) == 1

    def test_stock_validation_out_of_stock(self):
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 999},
            format="json",
        )
        assert res.status_code == 400
        assert res.data["success"] is False
        assert "Out of stock" in res.data["message"]

    def test_soft_delete_product_validation(self):
        """Deleted products cannot be added to cart."""
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product_deleted.id, "quantity": 1},
            format="json",
        )
        assert res.status_code == 400
        assert res.data["success"] is False
        assert "no longer available" in res.data["message"]

    def test_inactive_product_validation(self):
        """Inactive products cannot be added to cart."""
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product_inactive.id, "quantity": 1},
            format="json",
        )
        assert res.status_code == 400
        assert res.data["success"] is False
        assert "inactive" in res.data["message"]

    def test_totals_numeric_types(self):
        """Totals should be Decimal, not strings."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        res = self.client.get("/api/cart/")
        data = res.data["data"]
        
        assert isinstance(data["subtotal"], (int, float))
        assert isinstance(data["tax"], (int, float))
        assert isinstance(data["shipping"], (int, float))
        assert isinstance(data["total"], (int, float))

    def test_totals_calculation(self):
        """Verify tax and shipping calculations."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        res = self.client.get("/api/cart/")
        data = res.data["data"]
        
        assert Decimal(str(data["subtotal"])) == Decimal("400.00")
        assert Decimal(str(data["tax"])) == Decimal("56.00")
        assert Decimal(str(data["shipping"])) == Decimal("50.00")
        assert Decimal(str(data["total"])) == Decimal("506.00")

    def test_guest_cart_ownership_validation(self):
        """Different guest sessions cannot access each other's carts."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )

        res1 = self.client.get("/api/cart/")
        assert res1.status_code == 200
        assert len(res1.data["data"]["items"]) == 1

        self.client.cookies.clear()

        res2 = self.client.get("/api/cart/")
        assert res2.status_code == 200
        assert len(res2.data["data"]["items"]) == 0

    def test_authenticated_cart_ownership(self):
        """Authenticated users can only see their own cart."""
        other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="password123",
            role="customer",
        )

        self.client.force_authenticate(user=self.customer)
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        assert res.data["success"] is True
        
        customer_cart_id = Cart.objects.get(user=self.customer).id
        customer_item_count = len(res.data["data"]["items"])
        assert customer_item_count == 1

        self.client.force_authenticate(user=other)
        res2 = self.client.get("/api/cart/")
        assert len(res2.data["data"]["items"]) == 0

        res3 = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 5},
            format="json",
        )
        assert len(res3.data["data"]["items"]) == 1

        self.client.force_authenticate(user=self.customer)
        res4 = self.client.get("/api/cart/")
        assert len(res4.data["data"]["items"]) == 1

    def test_cart_item_update(self):
        """Update cart item quantity."""
        res_add = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        item_id = res_add.data["data"]["items"][0]["id"]

        res_update = self.client.patch(
            f"/api/cart/items/{item_id}/",
            {"quantity": 5},
            format="json",
        )
        assert res_update.status_code == 200
        assert res_update.data["success"] is True
        assert res_update.data["data"]["items"][0]["quantity"] == 5

    def test_cart_item_update_exceeds_stock(self):
        """Cannot update quantity beyond available stock."""
        res_add = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        item_id = res_add.data["data"]["items"][0]["id"]

        res_update = self.client.patch(
            f"/api/cart/items/{item_id}/",
            {"quantity": 999},
            format="json",
        )
        assert res_update.status_code == 400
        assert res_update.data["success"] is False

    def test_cart_item_delete(self):
        """Delete cart item."""
        res_add = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        item_id = res_add.data["data"]["items"][0]["id"]

        res_delete = self.client.delete(
            f"/api/cart/items/{item_id}/",
        )
        assert res_delete.status_code == 200
        assert res_delete.data["success"] is True

        res_check = self.client.get("/api/cart/")
        assert len(res_check.data["data"]["items"]) == 0

    def test_clear_cart(self):
        """Clear all items from cart."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        res_clear = self.client.delete("/api/cart/clear/")
        assert res_clear.status_code == 200
        assert res_clear.data["success"] is True

        res_check = self.client.get("/api/cart/")
        assert len(res_check.data["data"]["items"]) == 0

    def test_standardized_error_response_format(self):
        """All errors should follow standardized format."""
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": 99999, "quantity": 1},
            format="json",
        )
        assert res.status_code == 400
        assert res.data["success"] is False
        assert "message" in res.data

    def test_invalid_quantity_validation(self):
        """Invalid quantity values should be rejected."""
        res = self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 0},
            format="json",
        )
        assert res.status_code == 400
        assert res.data["success"] is False

    def test_line_subtotal_calculation(self):
        """Line subtotal should be calculated correctly."""
        self.client.post(
            "/api/cart/items/",
            {"product_id": self.product.id, "quantity": 3},
            format="json",
        )

        res = self.client.get("/api/cart/")
        item = res.data["data"]["items"][0]
        expected_line_subtotal = Decimal("200.00") * 3
        assert Decimal(str(item["line_subtotal"])) == expected_line_subtotal

        assert res2.data["success"] is True
        assert res2.data["data"]["items"] == []

