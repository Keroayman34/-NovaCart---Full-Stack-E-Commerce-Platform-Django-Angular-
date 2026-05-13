import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.reviews.models import Review
from apps.wishlist.models import Wishlist
from apps.notifications.models import Notification

User = get_user_model()

# List to store all created users for the credentials file
users_data = []

def seed_users():
    """Create multiple users with different roles"""
    global users_data
    users_data = []
    
    # Admin users
    admin_user, created = User.objects.get_or_create(
        email='admin@novacart.com',
        defaults={
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Admin',
            'last_name': 'User',
            'is_verified': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Admin user created")
    users_data.append({'email': 'admin@novacart.com', 'password': 'admin123', 'role': 'admin', 'username': 'admin'})

    # Seller users
    for i in range(5):
        seller_user, created = User.objects.get_or_create(
            email=f'seller{i+1}@novacart.com',
            defaults={
                'role': 'seller',
                'first_name': f'Seller',
                'last_name': f'{i+1}',
                'is_verified': True,
            }
        )
        if created:
            seller_user.set_password(f'seller{i+1}123')
            seller_user.save()
            print(f"✓ Seller {i+1} user created")
        users_data.append({'email': f'seller{i+1}@novacart.com', 'password': f'seller{i+1}123', 'role': 'seller', 'username': f'seller{i+1}'})

    # Customer users
    customer_names = [
        ('John', 'Doe'), ('Jane', 'Smith'), ('Ahmed', 'Hassan'), ('Maria', 'Garcia'),
        ('David', 'Johnson'), ('Sarah', 'Williams'), ('Ali', 'Khan'), ('Emma', 'Brown'),
        ('Michael', 'Davis'), ('Lisa', 'Rodriguez'), ('Omar', 'Ibrahim'), ('Sofia', 'Martinez'),
        ('James', 'Taylor'), ('Anna', 'Anderson'), ('Hassan', 'Mohamed'), ('Olivia', 'Thomas'),
    ]
    
    for i, (first, last) in enumerate(customer_names):
        customer_user, created = User.objects.get_or_create(
            email=f'customer{i+1}@novacart.com',
            defaults={
                'role': 'customer',
                'first_name': first,
                'last_name': last,
                'is_verified': True,
            }
        )
        if created:
            customer_user.set_password(f'customer{i+1}123')
            customer_user.save()
            print(f"✓ Customer {i+1} ({first} {last}) created")
        users_data.append({'email': f'customer{i+1}@novacart.com', 'password': f'customer{i+1}123', 'role': 'customer', 'username': f'customer{i+1}'})

def seed_categories():
    """Create product categories"""
    categories_data = [
        {'name': 'Electronics', 'description': 'Gadgets, phones, laptops and more'},
        {'name': 'Fashion', 'description': 'Clothing, shoes and accessories'},
        {'name': 'Home & Garden', 'description': 'Furniture, decor and garden equipment'},
        {'name': 'Sports', 'description': 'Fitness gear and outdoor equipment'},
        {'name': 'Books', 'description': 'Physical and digital books'},
        {'name': 'Beauty', 'description': 'Cosmetics, skincare and personal care'},
        {'name': 'Toys & Games', 'description': 'Toys, games and entertainment'},
        {'name': 'Automotive', 'description': 'Car accessories and parts'},
    ]

    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✓ Category '{cat.name}' created")
    
    return Category.objects.all()

def seed_products(categories, sellers):
    """Create products across categories"""
    if not sellers:
        print("ERROR: No sellers available. Products cannot be created without sellers.")
        return Product.objects.all()
    
    products_data = [
        # Electronics
        {'name': 'iPhone 15 Pro', 'price': 999.99, 'category': 'Electronics', 'sku': 'IPH15P001', 'desc': 'Latest Apple flagship phone'},
        {'name': 'Samsung Galaxy S24', 'price': 899.99, 'category': 'Electronics', 'sku': 'SGS24001', 'desc': 'Premium Android smartphone'},
        {'name': 'MacBook Air M3', 'price': 1199.99, 'category': 'Electronics', 'sku': 'MBA3M001', 'desc': 'Powerful laptop for professionals'},
        {'name': 'iPad Pro 12.9', 'price': 1099.99, 'category': 'Electronics', 'sku': 'IPADP12901', 'desc': 'Large-screen tablet'},
        {'name': 'Wireless Headphones', 'price': 199.99, 'category': 'Electronics', 'sku': 'WHP001', 'desc': 'Premium noise-cancelling headphones'},
        {'name': 'USB-C Hub', 'price': 79.99, 'category': 'Electronics', 'sku': 'USBCH001', 'desc': 'Multi-port connectivity hub'},
        {'name': 'Mechanical Keyboard', 'price': 149.99, 'category': 'Electronics', 'sku': 'MECH001', 'desc': 'High-performance gaming keyboard'},
        {'name': 'Gaming Mouse', 'price': 89.99, 'category': 'Electronics', 'sku': 'GMOUSE001', 'desc': 'Precision gaming mouse'},
        {'name': '4K Webcam', 'price': 129.99, 'category': 'Electronics', 'sku': 'WEBCAM4K001', 'desc': 'Ultra HD webcam for streaming'},
        {'name': 'Smart Watch', 'price': 399.99, 'category': 'Electronics', 'sku': 'SWATCH001', 'desc': 'Feature-rich smartwatch'},
        
        # Fashion
        {'name': 'Leather Jacket', 'price': 250.00, 'category': 'Fashion', 'sku': 'LJ001', 'desc': 'Premium genuine leather jacket'},
        {'name': 'Running Shoes', 'price': 120.00, 'category': 'Fashion', 'sku': 'RS001', 'desc': 'Professional running footwear'},
        {'name': 'Canvas Backpack', 'price': 45.00, 'category': 'Fashion', 'sku': 'CB001', 'desc': 'Durable canvas backpack'},
        {'name': 'Winter Coat', 'price': 180.00, 'category': 'Fashion', 'sku': 'WC001', 'desc': 'Warm winter outerwear'},
        {'name': 'Jeans', 'price': 70.00, 'category': 'Fashion', 'sku': 'JEANS001', 'desc': 'Classic denim jeans'},
        {'name': 'Dress Shoes', 'price': 95.00, 'category': 'Fashion', 'sku': 'DS001', 'desc': 'Elegant formal shoes'},
        {'name': 'Casual Tee', 'price': 25.00, 'category': 'Fashion', 'sku': 'TEE001', 'desc': 'Comfortable casual t-shirt'},
        {'name': 'Wool Sweater', 'price': 60.00, 'category': 'Fashion', 'sku': 'WS001', 'desc': 'Cozy wool sweater'},
        
        # Home & Garden
        {'name': 'Coffee Table', 'price': 150.00, 'category': 'Home & Garden', 'sku': 'CT001', 'desc': 'Modern coffee table'},
        {'name': 'Ergonomic Chair', 'price': 300.00, 'category': 'Home & Garden', 'sku': 'EC001', 'desc': 'Office ergonomic chair'},
        {'name': 'Desk Lamp', 'price': 45.00, 'category': 'Home & Garden', 'sku': 'DL001', 'desc': 'LED desk lamp'},
        {'name': 'Bookshelf', 'price': 120.00, 'category': 'Home & Garden', 'sku': 'BS001', 'desc': 'Wooden bookshelf'},
        {'name': 'Garden Tools Set', 'price': 55.00, 'category': 'Home & Garden', 'sku': 'GTS001', 'desc': 'Complete garden tools'},
        {'name': 'Bed Frame', 'price': 400.00, 'category': 'Home & Garden', 'sku': 'BF001', 'desc': 'Queen size bed frame'},
        
        # Sports
        {'name': 'Yoga Mat', 'price': 25.00, 'category': 'Sports', 'sku': 'YM001', 'desc': 'Non-slip yoga mat'},
        {'name': 'Dumbbell Set', 'price': 80.00, 'category': 'Sports', 'sku': 'DS001B', 'desc': 'Adjustable dumbbell set'},
        {'name': 'Treadmill', 'price': 600.00, 'category': 'Sports', 'sku': 'TM001', 'desc': 'Home treadmill'},
        {'name': 'Resistance Bands', 'price': 30.00, 'category': 'Sports', 'sku': 'RB001', 'desc': 'Set of resistance bands'},
        {'name': 'Bicycle', 'price': 350.00, 'category': 'Sports', 'sku': 'BIKE001', 'desc': 'Mountain bike'},
        
        # Books
        {'name': 'Python Programming', 'price': 45.00, 'category': 'Books', 'sku': 'PYPROG001', 'desc': 'Learn Python programming'},
        {'name': 'Clean Code', 'price': 42.00, 'category': 'Books', 'sku': 'CC001', 'desc': 'Guide to writing clean code'},
        
        # Beauty
        {'name': 'Face Moisturizer', 'price': 35.00, 'category': 'Beauty', 'sku': 'FM001', 'desc': 'Hydrating face moisturizer'},
        {'name': 'Lipstick Set', 'price': 25.00, 'category': 'Beauty', 'sku': 'LS001', 'desc': 'Multi-shade lipstick set'},
        
        # Toys & Games
        {'name': 'Board Game', 'price': 40.00, 'category': 'Toys & Games', 'sku': 'BG001', 'desc': 'Popular board game'},
        {'name': 'Puzzle Set', 'price': 20.00, 'category': 'Toys & Games', 'sku': 'PZ001', 'desc': '1000-piece puzzle'},
    ]

    product_count = 0
    for prod_data in products_data:
        category = Category.objects.get(name=prod_data['category'])
        seller = random.choice(sellers)
        
        prod, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults={
                'name': prod_data['name'],
                'price': Decimal(str(prod_data['price'])),
                'category': category,
                'seller': seller,
                'description': prod_data['desc'],
                'stock_quantity': random.randint(20, 200),
                'is_active': True,
            }
        )
        if created:
            product_count += 1
            print(f"✓ Product '{prod.name}' created")
    
    print(f"Total: {product_count} new products created")
    return Product.objects.all()

def seed_carts_and_items(customers, products):
    """Create carts with items"""
    carts_created = 0
    items_created = 0
    
    for customer in customers[:10]:  # Create carts for first 10 customers
        cart, created = Cart.objects.get_or_create(
            user=customer,
            defaults={}
        )
        if created:
            carts_created += 1
            # Add 2-5 items to cart
            num_items = random.randint(2, 5)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': random.randint(1, 3)}
                )
                items_created += 1
            print(f"✓ Cart created for {customer.first_name} {customer.last_name} with {num_items} items")
    
    print(f"Carts: {carts_created} | Items: {items_created}")

def seed_orders(customers, products):
    """Create orders with items"""
    order_count = 0
    order_items_count = 0
    
    statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    for customer in customers:
        # Create 1-3 orders per customer
        num_orders = random.randint(1, 3)
        
        for _ in range(num_orders):
            order = Order.objects.create(
                user=customer,
                status=random.choice(statuses),
                address=f"{random.randint(100, 9999)} Main Street, City {random.randint(1, 50)}, Country",
                total_price=Decimal(0),
                created_at=datetime.now() - timedelta(days=random.randint(0, 60))
            )
            order_count += 1
            
            # Add 2-5 items to order
            num_items = random.randint(2, 5)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            total = Decimal(0)
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
                order_items_count += 1
            
            order.total_price = total
            order.save()
        
        print(f"✓ Created {num_orders} orders for {customer.first_name} {customer.last_name}")
    
    print(f"Orders: {order_count} | Order Items: {order_items_count}")

def seed_reviews(customers, products):
    """Create product reviews"""
    reviews_created = 0
    
    for customer in customers:
        # Each customer reviews 2-5 products
        num_reviews = random.randint(2, 5)
        selected_products = random.sample(list(products), min(num_reviews, len(products)))
        
        for product in selected_products:
            review, created = Review.objects.get_or_create(
                user=customer,
                product=product,
                defaults={
                    'rating': random.randint(3, 5),
                    'comment': f"Great product! Highly recommended. Quality is {['excellent', 'good', 'very good'][random.randint(0, 2)]}.",
                    'created_at': datetime.now() - timedelta(days=random.randint(0, 30))
                }
            )
            if created:
                reviews_created += 1
        
        print(f"✓ Created reviews for {customer.first_name} {customer.last_name}")
    
    print(f"Total reviews: {reviews_created}")

def seed_wishlists(customers, products):
    """Create wishlists"""
    wishlists_created = 0
    
    for customer in customers:
        wishlist, created = Wishlist.objects.get_or_create(
            user=customer,
            defaults={}
        )
        
        # Add 3-7 products to wishlist
        num_items = random.randint(3, 7)
        selected_products = random.sample(list(products), min(num_items, len(products)))
        wishlist.products.set(selected_products)
        
        if created:
            wishlists_created += 1
        print(f"✓ Wishlist created for {customer.first_name} {customer.last_name} with {num_items} items")
    
    print(f"Total wishlists: {wishlists_created}")

def seed_notifications(customers):
    """Create notifications"""
    notification_types = ['order_confirmed', 'order_shipped', 'order_delivered', 'order_cancelled']
    notifications_created = 0
    
    for customer in customers:
        # Create 2-5 notifications per customer
        num_notifications = random.randint(2, 5)
        
        for _ in range(num_notifications):
            notif_type = random.choice(notification_types)
            messages = {
                'order_confirmed': 'Your order has been confirmed and will be shipped soon.',
                'order_shipped': 'Your order has been shipped! Track it now.',
                'order_delivered': 'Your order has been delivered. Thank you for shopping!',
                'order_cancelled': 'Your order has been cancelled.'
            }
            
            Notification.objects.create(
                user=customer,
                type=notif_type,
                message=messages[notif_type],
                is_read=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            notifications_created += 1
        
        print(f"✓ Created notifications for {customer.first_name} {customer.last_name}")
    
    print(f"Total notifications: {notifications_created}")

def save_users_to_file():
    """Save all user credentials to a text file"""
    file_path = '/home/abdullah/Desktop/E-Commerce/Backend/USER_CREDENTIALS.txt'
    
    with open(file_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("E-COMMERCE PLATFORM - USER LOGIN CREDENTIALS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Group by role
        admin_users = [u for u in users_data if u['role'] == 'admin']
        seller_users = [u for u in users_data if u['role'] == 'seller']
        customer_users = [u for u in users_data if u['role'] == 'customer']
        
        # Admin section
        f.write("ADMIN USERS\n")
        f.write("-" * 80 + "\n")
        for i, user in enumerate(admin_users, 1):
            f.write(f"{i}. Email: {user['email']}\n")
            f.write(f"   Password: {user['password']}\n")
            f.write(f"   Username: {user['username']}\n\n")
        
        # Seller section
        f.write("\n" + "=" * 80 + "\n")
        f.write("SELLER USERS\n")
        f.write("-" * 80 + "\n")
        for i, user in enumerate(seller_users, 1):
            f.write(f"{i}. Email: {user['email']}\n")
            f.write(f"   Password: {user['password']}\n")
            f.write(f"   Username: {user['username']}\n\n")
        
        # Customer section
        f.write("\n" + "=" * 80 + "\n")
        f.write("CUSTOMER USERS\n")
        f.write("-" * 80 + "\n")
        for i, user in enumerate(customer_users, 1):
            f.write(f"{i}. Email: {user['email']}\n")
            f.write(f"   Password: {user['password']}\n")
            f.write(f"   Username: {user['username']}\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Total Users: {len(users_data)}\n")
        f.write(f"  - Admins: {len(admin_users)}\n")
        f.write(f"  - Sellers: {len(seller_users)}\n")
        f.write(f"  - Customers: {len(customer_users)}\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n✓ User credentials saved to: {file_path}")

def seed_data():
    """Main seeding function"""
    print("\n" + "=" * 80)
    print("SEEDING E-COMMERCE DATABASE WITH COMPREHENSIVE DATA")
    print("=" * 80 + "\n")
    
    # Clear existing data (optional - uncomment if needed)
    # User.objects.all().delete()
    # Category.objects.all().delete()
    
    print("Step 1: Creating users...")
    print("-" * 80)
    seed_users()
    
    print("\n\nStep 2: Creating categories...")
    print("-" * 80)
    categories = seed_categories()
    
    print("\n\nStep 3: Creating products...")
    print("-" * 80)
    sellers = list(User.objects.filter(role='seller'))
    products = seed_products(categories, sellers)
    
    print("\n\nStep 4: Creating carts...")
    print("-" * 80)
    customers = list(User.objects.filter(role='customer'))
    seed_carts_and_items(customers, products)
    
    print("\n\nStep 5: Creating orders...")
    print("-" * 80)
    seed_orders(customers, products)
    
    print("\n\nStep 6: Creating reviews...")
    print("-" * 80)
    seed_reviews(customers, products)
    
    print("\n\nStep 7: Creating wishlists...")
    print("-" * 80)
    seed_wishlists(customers, products)
    
    print("\n\nStep 8: Creating notifications...")
    print("-" * 80)
    seed_notifications(customers)
    
    print("\n\nStep 9: Saving user credentials to file...")
    print("-" * 80)
    save_users_to_file()
    
    print("\n" + "=" * 80)
    print("✓ SEEDING COMPLETE!")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    seed_data()
