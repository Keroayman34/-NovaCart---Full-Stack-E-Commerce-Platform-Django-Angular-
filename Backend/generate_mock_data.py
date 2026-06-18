import os
import django
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Product, Category
from apps.orders.models import Order, OrderItem

User = get_user_model()

# 1. Get the seller user
try:
    seller = User.objects.get(email='abdullahelsman294@gmail.com')
except User.DoesNotExist:
    print("Seller not found.")
    exit(1)

# 2. Create some categories if none exist
cat1, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
cat2, _ = Category.objects.get_or_create(name='Clothing', slug='clothing')

# 3. Create mock products for the seller
products = []
for i in range(1, 10):
    prod, created = Product.objects.get_or_create(
        name=f'Wireless Headphones Model {i}',
        seller=seller,
        defaults={
            'description': f'High quality wireless headphones. Model {i}',
            'price': Decimal(f'{random.randint(50, 200)}.00'),
            'stock_quantity': random.randint(10, 100),
            'sku': f'SKU-MOCK-{i}',
            'category': cat1,
            'is_active': True,
            'average_rating': Decimal(f'{random.uniform(3.5, 5.0):.2f}')
        }
    )
    products.append(prod)

# 4. Create a mock customer
customer, _ = User.objects.get_or_create(
    email='mock_customer@example.com',
    defaults={'role': 'buyer', 'is_active': True, 'is_verified': True}
)
if not customer.password:
    customer.set_password('password123')
    customer.save()

# 5. Create some mock orders
status_choices = ['pending', 'confirmed', 'shipped', 'delivered', 'delivered'] # extra delivered for sales
for i in range(15):
    order = Order.objects.create(
        user=customer,
        address='123 Mock Street, Mock City',
        total_price=Decimal('0.00'),
        status=random.choice(status_choices)
    )
    
    # Add items to order
    order_total = Decimal('0.00')
    num_items = random.randint(1, 4)
    order_products = random.sample(products, num_items)
    
    for prod in order_products:
        qty = random.randint(1, 3)
        price = prod.price
        OrderItem.objects.create(
            order=order,
            product=prod,
            quantity=qty,
            price=price
        )
        order_total += price * qty
        
    order.total_price = order_total
    order.save()

print("Mock data generated successfully!")
