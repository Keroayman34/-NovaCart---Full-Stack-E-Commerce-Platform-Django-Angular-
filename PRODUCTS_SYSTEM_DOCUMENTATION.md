# NovaCart Product & Category System - Complete Implementation

## Overview

This document describes the complete implementation of the **Product & Category System** for the NovaCart e-commerce platform. The system follows production-ready best practices with clean architecture, comprehensive testing, and optimized performance.

## Architecture

### Directory Structure

```
backend/apps/products/
├── __init__.py
├── apps.py                 # App configuration
├── admin.py                # Django admin interface
├── models.py               # Database models (Category, Product, ProductImage)
├── serializers.py          # DRF serializers
├── services.py             # Business logic layer
├── permissions.py          # Custom permission classes
├── filters.py              # Filtering and search
├── views.py                # ViewSets
├── urls.py                 # URL routing
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Model tests
│   ├── test_views.py       # API endpoint tests
│   └── test_services.py    # Service layer tests
```

### Core Components

#### 1. Models (models.py)

**Category Model**
- Fields: name, slug, description, image, is_active, created_at, updated_at
- Features:
  - Auto-generated unique slugs
  - Soft validation for duplicate names
  - Database indexes for performance
  - Relationships with Products

**Product Model**
- Fields: category, seller, name, slug, description, sku, price, stock_quantity, is_active, is_deleted, created_at, updated_at
- Features:
  - Auto-generated unique slugs
  - Unique SKU constraint (when not deleted)
  - Soft delete support (is_deleted flag)
  - Price and stock validation
  - Seller-based ownership
  - N+1 query optimization with indexes

**ProductImage Model**
- Fields: product, image, is_primary, alt_text, created_at
- Features:
  - Multiple images per product
  - One primary image per product (automatic enforcement)
  - Accessibility support (alt_text)
  - Optimized ordering

#### 2. Serializers (serializers.py)

**CategorySerializer**
- Full CRUD serialization
- Includes product count
- Auto-generated URLs

**ProductListSerializer**
- Optimized for list views (minimal payload)
- Includes primary image
- Seller and category names

**ProductSerializer**
- Full product data
- Nested images
- Seller selection (admin only)
- Ownership information

**ProductDetailSerializer**
- Extended ProductSerializer
- Nested category object
- Full image details

**ProductImageSerializer**
- Image CRUD operations
- Primary image flag

#### 3. Service Layer (services.py)

**CategoryService**
- `create_category()` - Create with validation
- `update_category()` - Update with validation
- `delete_category()` - Soft delete
- `activate_category()` - Activate category

**ProductService**
- `generate_slug()` - Unique slug generation
- `create_product()` - Create with validation
- `update_product()` - Update with validation
- `soft_delete_product()` - Soft delete
- `restore_product()` - Restore deleted product
- `update_stock()` - Stock management with validation
- `deactivate_product()` / `activate_product()` - Visibility control

**ProductImageService**
- `add_image()` - Add image with validation
- `remove_image()` - Delete image
- `set_primary_image()` - Set primary (auto-unsets others)
- `get_primary_image()` - Retrieve primary

#### 4. Permissions (permissions.py)

**IsAdminOrReadOnly**
- Admins: Full access
- Others: Read-only

**IsSellerOrAdmin**
- Sellers: Create products, edit/delete own
- Admins: Full access
- Customers: Read-only

**IsCategoryAdmin**
- Admins: Full access
- Others: Read-only

**IsProductOwnerOrAdmin**
- Owners: Modify their products
- Admins: Modify any product

**IsReadOnlyCustomer**
- Customers: Read-only access

#### 5. Filters (filters.py)

**CategoryFilter**
- is_active filter
- Name search (case-insensitive)

**ProductFilter**
- Category filtering (by ID or slug)
- Price range filtering (min/max)
- Seller filtering
- Stock status filtering
- SKU search

**ProductSearchFilter**
- Search: name, description, SKU

**ProductOrderingFilter**
- Order by: price, created_at, name, stock_quantity
- Both ascending and descending

#### 6. ViewSets (views.py)

**CategoryViewSet**
- List, Create, Retrieve, Update, Delete (Destroy disabled, uses soft delete via action)
- Custom actions:
  - `by_slug` - Get by slug
  - `activate` - Activate category
  - `deactivate` - Deactivate category
- Pagination with metadata
- Filtering and ordering
- Role-based access control

**ProductViewSet**
- Full CRUD operations
- Query optimization (select_related, prefetch_related)
- Custom actions:
  - `by_slug` - Get by slug
  - `upload_image` - Upload product image
  - `set_primary_image` - Set primary image
  - `delete_image` - Delete image
  - `update_stock` - Update stock quantity
  - `restore` - Restore deleted product
- Soft delete support
- Role-based queries
- Filtering, searching, ordering
- Pagination with metadata

#### 7. Pagination (core/pagination.py)

**CustomPagination**
- Page size: 10 (configurable)
- Client override support
- Metadata included:
  - total_items
  - total_pages
  - current_page
  - page_size
- Consistent response format

## API Endpoints

### Category Endpoints

```
GET    /api/categories/                    # List categories
POST   /api/categories/                    # Create category (admin)
GET    /api/categories/{id}/               # Get by ID
GET    /api/categories/by_slug/?slug=...   # Get by slug
PATCH  /api/categories/{id}/               # Update (admin)
DELETE /api/categories/{id}/               # Soft delete (admin)
POST   /api/categories/{id}/activate/      # Activate (admin)
POST   /api/categories/{id}/deactivate/    # Deactivate (admin)
```

### Product Endpoints

```
GET    /api/products/                           # List products (with filters)
POST   /api/products/                           # Create product (seller/admin)
GET    /api/products/{id}/                      # Get by ID
GET    /api/products/by_slug/?slug=...          # Get by slug
PATCH  /api/products/{id}/                      # Update (owner/admin)
DELETE /api/products/{id}/                      # Soft delete (owner/admin)
POST   /api/products/{id}/upload_image/         # Upload image
POST   /api/products/{id}/set_primary_image/    # Set primary image
POST   /api/products/{id}/delete_image/         # Delete image
POST   /api/products/{id}/update_stock/         # Update stock
POST   /api/products/{id}/restore/              # Restore (admin)
```

## Query Parameters

### Filtering

```
# Category filtering
/api/categories/?is_active=true
/api/categories/?name=electronics

# Product filtering
/api/products/?category=1                    # By category ID
/api/products/?category_slug=electronics    # By category slug
/api/products/?seller=1                     # By seller ID
/api/products/?price_min=100                # Minimum price
/api/products/?price_max=500                # Maximum price
/api/products/?sku=IPHONE13                # By SKU
/api/products/?in_stock=true               # In stock only
/api/products/?is_active=true              # Active products
```

### Searching

```
/api/products/?search=iphone           # Search name, description, SKU
```

### Ordering

```
/api/products/?ordering=price          # Ascending price
/api/products/?ordering=-price         # Descending price
/api/products/?ordering=-created_at    # Newest first
/api/products/?ordering=name           # By name A-Z
```

### Pagination

```
/api/products/?page=1               # First page
/api/products/?page=2&page_size=20  # Page 2 with custom size
```

## Request/Response Examples

### Create Product (POST /api/products/)

**Request:**
```json
{
  "name": "iPhone 13 Pro",
  "sku": "IPHONE13PRO",
  "price": 999.99,
  "stock_quantity": 50,
  "category_id": 1,
  "description": "Latest iPhone model",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "iPhone 13 Pro",
    "slug": "iphone-13-pro",
    "sku": "IPHONE13PRO",
    "price": "999.99",
    "stock_quantity": 50,
    "is_in_stock": true,
    "category": {
      "id": 1,
      "name": "Electronics",
      "slug": "electronics"
    },
    "seller_name": "seller@example.com",
    "images": [],
    "is_owned_by_user": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### List Products (GET /api/products/?search=iphone&ordering=-price)

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "iPhone 13 Pro",
        "slug": "iphone-13-pro",
        "price": "999.99",
        "is_in_stock": true,
        "category_name": "Electronics",
        "primary_image": {
          "id": 1,
          "image": "/media/products/2024/01/image.jpg",
          "is_primary": true
        }
      }
    ],
    "pagination": {
      "total_items": 2,
      "total_pages": 1,
      "current_page": 1,
      "page_size": 10
    }
  }
}
```

### Upload Product Image (POST /api/products/1/upload_image/)

**Request:**
```json
{
  "image": <file>,
  "is_primary": true,
  "alt_text": "iPhone 13 Pro main image"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "image": "/media/products/2024/01/image.jpg",
    "is_primary": true,
    "alt_text": "iPhone 13 Pro main image"
  }
}
```

### Update Stock (POST /api/products/1/update_stock/)

**Request:**
```json
{
  "quantity_change": -5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "stock_quantity": 45,
    "is_in_stock": true
  }
}
```

## Access Control

### Category Operations
- **Read**: Authenticated users (customers, sellers, admins)
- **Create/Update/Delete**: Admins only

### Product Operations
| Operation | Customer | Seller | Admin |
|-----------|----------|--------|-------|
| List (active) | ✓ | ✓ (+ own) | ✓ |
| Create | ✗ | ✓ | ✓ |
| Read (own/active) | ✓ (active) | ✓ | ✓ |
| Update | ✗ | ✓ (own) | ✓ |
| Delete (soft) | ✗ | ✓ (own) | ✓ |
| Upload Image | ✗ | ✓ (own) | ✓ |
| Update Stock | ✗ | ✓ (own) | ✓ |

## Performance Optimizations

### Database Optimizations

1. **Indexing**
   - Slug fields indexed
   - Foreign keys indexed
   - Composite indexes for common queries
   - Soft delete awareness in unique constraints

2. **Query Optimization**
   - `select_related()` for ForeignKeys (category, seller)
   - `prefetch_related()` for reverse relations (images)
   - Pagination to limit result sets
   - Filtered querysets at database level

3. **Caching Ready**
   - Slug-based lookups for better cache hits
   - Immutable primary images

### API Optimizations

1. **Pagination**
   - Default page size: 10
   - Configurable up to 100
   - Metadata for efficient client-side navigation

2. **Serializers**
   - Optimized list serializer (smaller payload)
   - Full detail serializer for detail views
   - Nested representations minimize requests

## Validation

### Model-Level Validation
- Price > 0
- Stock quantity >= 0
- Category required
- Unique SKU per non-deleted product
- Unique slug per product
- One primary image per product
- Category name uniqueness (case-insensitive)

### Serializer-Level Validation
- All required fields validated
- Field constraints enforced
- Custom validation logic

### Business Logic Validation
- Service layer validates before persistence
- Transaction safety for multi-step operations
- Cascading deletes prevented (PROTECT on category)

## Testing

### Test Coverage

**test_models.py** (16 test cases)
- Category creation and validation
- Product creation, validation, soft delete
- ProductImage handling and primary image logic
- Slug generation and uniqueness
- Stock validation
- Ownership validation

**test_views.py** (18 test cases)
- List/Create/Retrieve/Update/Delete endpoints
- Permission-based access control
- Filtering, searching, ordering
- Soft delete operations
- Image upload operations
- Stock updates
- Seller ownership validation

**test_services.py** (19 test cases)
- Service layer business logic
- Slug generation uniqueness
- Product CRUD operations
- Stock management
- Soft delete and restore
- Image operations
- Error handling

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-django

# Run all tests
pytest

# Run specific test file
pytest apps/products/tests/test_models.py

# Run with coverage
pytest --cov=apps.products

# Run specific test
pytest apps/products/tests/test_models.py::TestProductModel::test_create_product
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install django django-rest-framework djangorestframework-simplejwt django-filter pillow
```

### 2. Add to settings.py

```python
INSTALLED_APPS = [
    # ... other apps
    'django_filters',
    'apps.products',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPagination',
}
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Access Admin

```
http://localhost:8000/admin/
```

## Error Handling

### Standard Error Response

```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field": ["Field-specific error"]
  }
}
```

### Common HTTP Status Codes

- `200 OK` - Successful GET/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource

## Future Enhancements

1. **Elasticsearch Integration** - Full-text search
2. **Caching** - Redis caching for frequently accessed products
3. **Rating System** - Reviews and star ratings
4. **Recommendations** - ML-based product recommendations
5. **Bulk Operations** - Bulk upload/update of products
6. **Advanced Analytics** - Sales metrics, trend analysis
7. **Inventory Alerts** - Low stock notifications
8. **Versioning** - API versioning support

## Conclusion

The Product & Category System is a production-ready implementation following Django and DRF best practices. It provides:

- ✅ Clean architecture with separation of concerns
- ✅ Comprehensive permission and access control
- ✅ Advanced filtering and search capabilities
- ✅ Optimized database queries
- ✅ Extensive test coverage
- ✅ Professional API responses
- ✅ Scalable design ready for growth
