import pytest
from decimal import Decimal

from apps.products.models import Category, Product
from apps.users.models import User

from apps.cart.models import Cart, CartItem
from apps.cart.services import CartService
from core.exceptions import OutOfStockException, ProductInactiveException


@pytest.mark.django_db
class TestCartMergeService:
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
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)

        CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

        assert Cart.objects.filter(id=guest_cart.id).exists() is False
        assert CartItem.objects.filter(cart=user_cart, product=self.product).get().quantity == 3

    def test_merge_cart_validates_stock_before_merge(self):
        """Merge fails if combined quantity exceeds stock."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=3)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=3)

        with pytest.raises(OutOfStockException):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

    def test_merge_cart_validates_deleted_products(self):
        """Merge fails if products are soft-deleted."""
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

        with pytest.raises(ProductInactiveException):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

    def test_merge_cart_validates_inactive_products(self):
        """Merge fails if products are inactive."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        inactive_product = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Inactive",
            sku="SKU-INACTIVE",
            price=Decimal("100.00"),
            stock_quantity=5,
            is_active=False,
            is_deleted=False,
        )

        CartItem.objects.create(cart=guest_cart, product=inactive_product, quantity=1)

        with pytest.raises(ProductInactiveException):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

    def test_merge_cart_creates_items_if_not_exist_in_user_cart(self):
        """Merge creates new items in user cart if they don't already exist."""
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
        assert CartItem.objects.get(cart=user_cart, product=self.product).quantity == 1
        assert CartItem.objects.get(cart=user_cart, product=product2).quantity == 1

    def test_merge_deletes_all_guest_items_after_merge(self):
        """All guest cart items are deleted after successful merge."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        product2 = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Tablet",
            sku="SKU-TABLET",
            price=Decimal("500.00"),
            stock_quantity=2,
            is_active=True,
            is_deleted=False,
        )

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=guest_cart, product=product2, quantity=1)

        assert CartItem.objects.filter(cart=guest_cart).count() == 2

        CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

        assert CartItem.objects.filter(cart=guest_cart).count() == 0

    def test_merge_cart_is_atomic(self):
        """Merge operation is atomic - either fully succeeds or fully fails."""
        guest_cart = Cart.objects.create(session_key="guest-session")
        user_cart = Cart.objects.create(user=self.customer)

        product2 = Product.objects.create(
            category=self.category,
            seller=self.seller,
            name="Laptop",
            sku="SKU-LAPTOP",
            price=Decimal("1000.00"),
            stock_quantity=1,
            is_active=True,
            is_deleted=False,
        )

        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=3)
        CartItem.objects.create(cart=guest_cart, product=product2, quantity=1)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=3)

        initial_guest_items = CartItem.objects.filter(cart=guest_cart).count()

        with pytest.raises(OutOfStockException):
            CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)

        assert CartItem.objects.filter(cart=guest_cart).count() == initial_guest_items
        assert Cart.objects.filter(id=guest_cart.id).exists()


