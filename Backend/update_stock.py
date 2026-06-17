import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

def update_test_stock():
    # Make iPhone 15 Pro out of stock
    p1 = Product.objects.get(id=1)
    p1.stock_quantity = 0
    p1.save()
    print(f"Set '{p1.name}' to Out of Stock (0)")

    # Make Samsung Galaxy S24 low stock
    p2 = Product.objects.get(id=2)
    p2.stock_quantity = 2
    p2.save()
    print(f"Set '{p2.name}' to Low Stock (2)")

    # Make MacBook Air M3 out of stock
    p3 = Product.objects.get(id=3)
    p3.stock_quantity = 0
    p3.save()
    print(f"Set '{p3.name}' to Out of Stock (0)")

    # Make iPad Pro 12.9 low stock
    p4 = Product.objects.get(id=4)
    p4.stock_quantity = 1
    p4.save()
    print(f"Set '{p4.name}' to Low Stock (1)")

if __name__ == '__main__':
    update_test_stock()
