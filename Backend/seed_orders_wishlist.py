import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.wishlist.models import Wishlist
from apps.orders.models import Order, OrderItem

User = get_user_model()

def seed_data():
    user = User.objects.filter(is_superuser=False).first()
    if not user:
        print("No normal user found. Creating a test user...")
        user = User.objects.create_user(email="testuser@example.com", password="password123", role="customer", is_verified=True)
        print(f"Created test user: {user.email}")
    else:
        print(f"Using existing user: {user.email}")

    products = list(Product.objects.all()[:10])
    if not products:
        print("No products found to seed data.")
        return

    # Seed Wishlist
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    if not wishlist.products.exists():
        wishlist_items = random.sample(products, 3)
        wishlist.products.add(*wishlist_items)
        print(f"Added {len(wishlist_items)} products to wishlist.")
    else:
        print("Wishlist already has products.")

    # Seed Orders
    if user.orders.count() == 0:
        for i in range(2):
            order = Order.objects.create(
                user=user,
                status=random.choice(['delivered', 'shipped', 'pending']),
                total_price=0,
                address="123 Example Street, Test City, 12345"
            )
            
            order_items = random.sample(products, random.randint(1, 3))
            total = Decimal(0)
            for product in order_items:
                quantity = random.randint(1, 2)
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
            
            order.total_price = total
            order.save()
            print(f"Created order #{order.id} with total ${total}.")
    else:
        print(f"User already has {user.orders.count()} orders.")

if __name__ == '__main__':
    seed_data()
