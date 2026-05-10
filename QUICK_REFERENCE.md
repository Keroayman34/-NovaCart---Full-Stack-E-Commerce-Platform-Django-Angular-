# Quick Reference - Product & Category System

## Running the Application

```bash
# Install dependencies
pip install django django-rest-framework djangorestframework-simplejwt django-filter pillow pytest pytest-django

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Run tests
pytest
pytest --cov=apps.products
```

## API Quick Reference

### Authentication
All endpoints (except list) require JWT token:
```
Authorization: Bearer <token>
```

### Categories

| Method | Endpoint | Permission | Description |
|--------|----------|-----------|-------------|
| GET | `/api/categories/` | Any | List categories |
| POST | `/api/categories/` | Admin | Create category |
| GET | `/api/categories/{id}/` | Any | Get category |
| PATCH | `/api/categories/{id}/` | Admin | Update category |
| DELETE | `/api/categories/{id}/` | Admin | Delete category |

### Products

| Method | Endpoint | Permission | Description |
|--------|----------|-----------|-------------|
| GET | `/api/products/` | Any | List products |
| POST | `/api/products/` | Seller/Admin | Create product |
| GET | `/api/products/{id}/` | Any | Get product |
| PATCH | `/api/products/{id}/` | Owner/Admin | Update product |
| DELETE | `/api/products/{id}/` | Owner/Admin | Soft delete |
| POST | `/api/products/{id}/upload_image/` | Owner/Admin | Upload image |
| POST | `/api/products/{id}/set_primary_image/` | Owner/Admin | Set primary |
| POST | `/api/products/{id}/delete_image/` | Owner/Admin | Delete image |
| POST | `/api/products/{id}/update_stock/` | Owner/Admin | Update stock |

## Query Examples

```bash
# Search for products
curl "http://localhost:8000/api/products/?search=iphone"

# Filter by price
curl "http://localhost:8000/api/products/?price_min=100&price_max=500"

# Filter by category
curl "http://localhost:8000/api/products/?category=1"

# Order by price (descending)
curl "http://localhost:8000/api/products/?ordering=-price"

# Pagination
curl "http://localhost:8000/api/products/?page=1&page_size=20"

# Combined
curl "http://localhost:8000/api/products/?category=1&price_min=100&search=phone&ordering=-price&page=1"
```

## Create Examples

### Create Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 13",
    "sku": "IPHONE13",
    "price": 999.99,
    "stock_quantity": 10,
    "category_id": 1,
    "description": "Latest model"
  }'
```

### Upload Product Image
```bash
curl -X POST http://localhost:8000/api/products/1/upload_image/ \
  -H "Authorization: Bearer <token>" \
  -F "image=@/path/to/image.jpg" \
  -F "is_primary=true" \
  -F "alt_text=Product image"
```

### Update Stock
```bash
curl -X POST http://localhost:8000/api/products/1/update_stock/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"quantity_change": 5}'
```

## File Structure

```
backend/apps/products/
├── models.py              # Database models
├── serializers.py         # API serializers
├── services.py            # Business logic
├── views.py              # ViewSets
├── permissions.py        # Access control
├── filters.py            # Filtering
├── urls.py               # URL routing
├── admin.py              # Admin interface
├── apps.py               # App config
└── tests/                # Tests
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

## Common Issues

### Issue: Product not showing in list
**Solution**: Check if `is_active=True` and `is_deleted=False`

### Issue: Duplicate SKU error
**Solution**: SKU must be unique per non-deleted product

### Issue: Can't set two primary images
**Solution**: System automatically unsets previous primary image

### Issue: Seller can't edit other's product
**Solution**: Only product owner (seller) or admin can edit

### Issue: No pagination metadata
**Solution**: Make sure CustomPagination is set in settings

## Admin Interface

Access at: `http://localhost:8000/admin/`

All models are registered:
- Category
- Product
- ProductImage

Features:
- Search by name/SKU
- Filter by category, seller, status
- Inline image management
- Bulk actions

## Database Optimization

The system includes:
- Proper indexes on frequently queried fields
- select_related() for foreign keys
- prefetch_related() for reverse relations
- Soft deletes to avoid data loss
- Unique constraints with soft-delete awareness

## Performance Metrics

- Default page size: 10
- Max page size: 100
- Query optimization: select_related + prefetch_related
- Pagination: Reduces memory usage for large datasets

## Response Format

All API responses follow this format:

```json
{
  "success": true/false,
  "data": { /* response data */ },
  "pagination": { /* pagination info (if paginated) */ },
  "message": "Error message (if error)"
}
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/products/tests/test_models.py

# Run with coverage report
pytest --cov=apps.products --cov-report=html

# Run specific test
pytest apps/products/tests/test_models.py::TestProductModel::test_create_product

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## Key Services

### CategoryService
- `create_category(name, description, image)`
- `update_category(category, **kwargs)`
- `delete_category(category)`
- `activate_category(category)`

### ProductService
- `generate_slug(name, instance)`
- `create_product(category, seller, name, sku, price, stock, description, is_active)`
- `update_product(product, **kwargs)`
- `soft_delete_product(product)`
- `restore_product(product)`
- `update_stock(product, quantity_change)`
- `deactivate_product(product)`
- `activate_product(product)`

### ProductImageService
- `add_image(product, image, is_primary, alt_text)`
- `remove_image(product_image)`
- `set_primary_image(product, product_image)`
- `get_primary_image(product)`

## Permissions Quick Guide

| Role | Category | Product | Image |
|------|----------|---------|-------|
| Customer | Read | Read (active only) | N/A |
| Seller | Read | Create, Read (own), Update (own), Delete (own) | Upload (own) |
| Admin | Full | Full | Full |

---

For detailed documentation, see: `PRODUCTS_SYSTEM_DOCUMENTATION.md`
