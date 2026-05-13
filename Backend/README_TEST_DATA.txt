================================================================================
QUICK START GUIDE - E-COMMERCE DATABASE TEST DATA
================================================================================

✓ DATABASE SUCCESSFULLY POPULATED WITH TEST DATA
✓ ALL USERS, PRODUCTS, ORDERS, REVIEWS, AND RELATIONSHIPS CREATED
✓ LOGIN CREDENTIALS SAVED FOR TESTING

================================================================================
FILES CREATED
================================================================================

1. USER_CREDENTIALS.txt
   - Contains all 22 user login credentials (1 admin, 5 sellers, 16 customers)
   - Format: Email, Password, Username, Role
   - Use this file to login and test different user roles

2. DATABASE_SCHEMA.txt
   - Complete documentation of all 11 database tables
   - Table definitions, relationships, constraints
   - Indexing strategy and business rules
   - Field types and validation rules

3. SEEDING_REPORT.txt
   - Detailed report of seeding process
   - Data statistics and organization
   - How to use test data
   - Troubleshooting guide

4. seed.py (UPDATED)
   - Enhanced seed script with full data generation
   - Can be re-run to reset database with fresh test data
   - Creates all tables and relationships

5. db.sqlite3 (DATABASE)
   - SQLite database file with all test data
   - Contains 22 users, 35 products, 38 orders, 58 reviews, etc.
   - Ready for testing and development

================================================================================
QUICK STATS
================================================================================

USERS:
  ✓ 1 Admin
  ✓ 5 Sellers  
  ✓ 16 Customers
  Total: 22 users

PRODUCTS:
  ✓ 8 Categories
  ✓ 35 Products
  ✓ Price range: $20 - $1,199
  ✓ Stock: 20-200 units each

SHOPPING DATA:
  ✓ 10 Shopping Carts (35 items)
  ✓ 38 Orders (115 items)
  ✓ 58 Product Reviews
  ✓ 16 Wishlists
  ✓ 53 Notifications

================================================================================
ADMIN USER (for full access):
================================================================================

Email: admin@novacart.com
Password: admin123

Use this account to access the admin dashboard and manage all platform data.

================================================================================
SAMPLE SELLER USER:
================================================================================

Email: seller1@novacart.com
Password: seller1123

Use to test seller features:
- View own products
- Manage inventory
- Track orders

4 more sellers available: seller2 through seller5 (same password pattern)

================================================================================
SAMPLE CUSTOMER USER:
================================================================================

Email: customer1@novacart.com
Password: customer1123

Use to test customer features:
- Browse products
- Add to cart
- Place orders
- Leave reviews
- Create wishlists

15 more customers available: customer2 through customer16 (same pattern)

ALL CREDENTIALS IN USER_CREDENTIALS.txt

================================================================================
DATABASE TABLES (Total: 11 tables)
================================================================================

1. Users (22 records)
   - Admin, Sellers, Customers
   
2. Categories (8 records)
   - Electronics, Fashion, Home & Garden, Sports, Books, Beauty, 
     Toys & Games, Automotive
   
3. Products (35 records)
   - Distributed across categories
   - Assigned to sellers
   
4. Product Images (0 records - structure ready)
   - For product photos
   
5. Carts (10 records)
   - Customer shopping carts
   
6. Cart Items (35 records)
   - Products in carts
   
7. Orders (38 records)
   - Customer order history
   
8. Order Items (115 records)
   - Items in orders
   
9. Reviews (58 records)
   - Customer product reviews
   
10. Wishlists (16 records)
    - Customer wishlists (1 per customer)
    
11. Notifications (53 records)
    - Order notifications

================================================================================
TESTING THE SYSTEM
================================================================================

1. Start the Django development server:
   python venv/bin/python manage.py runserver

2. Access the API at: http://localhost:8000/

3. Admin panel at: http://localhost:8000/admin/
   Use admin credentials to login

4. Test user authentication with any credentials from USER_CREDENTIALS.txt

5. Test different user roles:
   - Admin: Full system access
   - Sellers: Manage products
   - Customers: Shop and review

================================================================================
RESETTING THE DATABASE
================================================================================

To reset with fresh test data:

1. Backup current database:
   cp db.sqlite3 db.sqlite3.backup

2. Delete old database:
   rm db.sqlite3

3. Apply migrations:
   python venv/bin/python manage.py migrate

4. Re-run seed script:
   python venv/bin/python seed.py

This will regenerate all test data from scratch.

================================================================================
QUERYING THE DATABASE
================================================================================

Start Django shell:
  python venv/bin/python manage.py shell

Example queries:

  # Get all users
  from django.contrib.auth import get_user_model
  User = get_user_model()
  users = User.objects.all()

  # Get all active products
  from apps.products.models import Product
  products = Product.objects.filter(is_active=True)

  # Get all orders
  from apps.orders.models import Order
  orders = Order.objects.all()

  # Get reviews for a product
  from apps.reviews.models import Review
  reviews = Review.objects.filter(product_id=1)

  # Get customer wishlists
  from apps.wishlist.models import Wishlist
  wishlists = Wishlist.objects.all()

================================================================================
PRODUCT CATEGORIES & INVENTORY
================================================================================

Electronics (10 products):
  - iPhone 15 Pro ($999.99)
  - Samsung Galaxy S24 ($899.99)
  - MacBook Air M3 ($1,199.99)
  - iPad Pro 12.9" ($1,099.99)
  - Wireless Headphones ($199.99)
  - USB-C Hub ($79.99)
  - Mechanical Keyboard ($149.99)
  - Gaming Mouse ($89.99)
  - 4K Webcam ($129.99)
  - Smart Watch ($399.99)

Fashion (8 products):
  - Leather Jacket ($250.00)
  - Running Shoes ($120.00)
  - Canvas Backpack ($45.00)
  - Winter Coat ($180.00)
  - Jeans ($70.00)
  - Dress Shoes ($95.00)
  - Casual Tee ($25.00)
  - Wool Sweater ($60.00)

Home & Garden (6 products):
  - Coffee Table ($150.00)
  - Ergonomic Chair ($300.00)
  - Desk Lamp ($45.00)
  - Bookshelf ($120.00)
  - Garden Tools Set ($55.00)
  - Bed Frame ($400.00)

Sports (5 products):
  - Yoga Mat ($25.00)
  - Dumbbell Set ($80.00)
  - Treadmill ($600.00)
  - Resistance Bands ($30.00)
  - Bicycle ($350.00)

Books (2 products):
  - Python Programming ($45.00)
  - Clean Code ($42.00)

Beauty (2 products):
  - Face Moisturizer ($35.00)
  - Lipstick Set ($25.00)

Toys & Games (2 products):
  - Board Game ($40.00)
  - Puzzle Set ($20.00)

================================================================================
KEY DATA RELATIONSHIPS
================================================================================

✓ Each Product belongs to a Category
✓ Each Product is owned by a Seller (User with role='seller')
✓ Each Customer can create multiple Orders
✓ Each Order contains multiple OrderItems (Products)
✓ Each Customer can leave one Review per Product
✓ Each Customer has one Wishlist with multiple Products
✓ Each Notification belongs to a User

All relationships are properly established and tested.

================================================================================
DOCUMENTATION FILES
================================================================================

For detailed information, see:

1. DATABASE_SCHEMA.txt
   - Full schema documentation
   - Table definitions and relationships
   - Indexing strategy
   - Business rules and constraints

2. SEEDING_REPORT.txt
   - Detailed seeding process report
   - Data organization guide
   - Performance considerations
   - Troubleshooting section

3. USER_CREDENTIALS.txt
   - All 22 user login credentials
   - Organized by role
   - Ready for API testing

================================================================================
COMMON TASKS
================================================================================

Login as Admin:
  - Email: admin@novacart.com
  - Password: admin123

Login as Seller:
  - Email: seller1@novacart.com
  - Password: seller1123

Login as Customer:
  - Email: customer1@novacart.com
  - Password: customer1123

Browse Products:
  - Use customer credentials
  - View all categories
  - Add items to cart

Manage Orders:
  - Admin can view all orders
  - Sellers can view their product orders
  - Customers can view their orders

View Reviews:
  - Each product has multiple reviews
  - Customers can add/edit reviews

Check Notifications:
  - 53 test notifications pre-created
  - Mix of read/unread status

================================================================================
SUPPORT & TROUBLESHOOTING
================================================================================

Issue: "User matching query does not exist"
Solution: Run seed.py again to populate users

Issue: "User credentials not working"
Solution: Check USER_CREDENTIALS.txt for exact format

Issue: "Products not showing"
Solution: Verify products are is_active=True

Issue: "Orders not visible"
Solution: Check user has proper role for viewing orders

Issue: "Database locked"
Solution: Restart Django server

For more help, see SEEDING_REPORT.txt troubleshooting section.

================================================================================
SUMMARY
================================================================================

✓ Database populated with realistic test data
✓ All 22 users created with verified emails
✓ 35 products across 8 categories ready for testing
✓ 38 orders with complete history
✓ 58 reviews from customers
✓ 16 wishlists from customers
✓ All relationships properly established
✓ Login credentials saved in USER_CREDENTIALS.txt
✓ Complete schema documentation in DATABASE_SCHEMA.txt
✓ Detailed report in SEEDING_REPORT.txt

Ready for API testing, manual testing, and development!

================================================================================
Generated: 2026-05-12
Status: ✓ COMPLETE AND READY FOR TESTING
================================================================================
