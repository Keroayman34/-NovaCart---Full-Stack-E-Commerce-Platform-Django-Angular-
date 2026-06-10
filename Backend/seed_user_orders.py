import os, django, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(id=24)
products = list(Product.objects.filter(is_active=True, is_deleted=False)[:6])

statuses = ['pending', 'confirmed', 'shipped', 'delivered']

for i in range(3):
    order = Order.objects.create(
        user=user,
        status=statuses[i],
        total_price=0,
        address='123 Test Street, Cairo, Egypt',
    )
    total = 0
    selected = random.sample(products, min(random.randint(2, 3), len(products)))
    for p in selected:
        qty = random.randint(1, 3)
        item_total = float(p.price) * qty
        OrderItem.objects.create(
            order=order,
            product=p,
            quantity=qty,
            price=p.price,
        )
        total += item_total
    order.total_price = total
    order.save()
    print(f'Created Order #{order.id} - status={order.status} total={order.total_price} items={len(selected)}')

print('Done! Created 3 orders for', user.email)
