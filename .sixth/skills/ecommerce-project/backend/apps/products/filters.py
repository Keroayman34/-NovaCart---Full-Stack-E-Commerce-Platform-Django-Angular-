"""
Filter classes for product and category queries.
"""
import django_filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Category


class CategoryFilter(django_filters.FilterSet):
    """
    Filter for Category model.
    
    Filters:
        - is_active: Filter by active status
        - search: Search by name or description
    """
    is_active = django_filters.BooleanFilter()
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Search by category name"
    )

    class Meta:
        model = Category
        fields = ["is_active", "name"]


class ProductFilter(django_filters.FilterSet):
    """
    Filter for Product model.
    
    Filters:
        - category: Filter by category ID or slug
        - seller: Filter by seller ID
        - price_min: Minimum price filter
        - price_max: Maximum price filter
        - is_active: Filter by active status
        - is_in_stock: Filter by stock status
        - search: Search by name, description, or SKU
        - ordering: Order by price, created_at, name
    """
    category = django_filters.NumberFilter(
        field_name="category__id",
        label="Category ID"
    )
    category_slug = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="exact",
        label="Category slug"
    )
    price_min = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Minimum price"
    )
    price_max = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Maximum price"
    )
    seller = django_filters.NumberFilter(
        field_name="seller__id",
        label="Seller ID"
    )
    is_active = django_filters.BooleanFilter(label="Is active")
    in_stock = django_filters.BooleanFilter(
        field_name="stock_quantity",
        method="filter_in_stock",
        label="In stock"
    )
    sku = django_filters.CharFilter(
        field_name="sku",
        lookup_expr="iexact",
        label="SKU"
    )

    class Meta:
        model = Product
        fields = [
            "category",
            "category_slug",
            "seller",
            "price_min",
            "price_max",
            "is_active",
            "in_stock",
            "sku",
        ]

    def filter_in_stock(self, queryset, name, value):
        """
        Filter products by stock status.
        
        Args:
            queryset: QuerySet to filter
            name: Filter field name
            value: True to filter in-stock products
        """
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)


class ProductSearchFilter(SearchFilter):
    """
    Extended search filter for products.
    
    Searches in:
        - name: Product name
        - description: Product description
        - sku: Stock Keeping Unit
    """
    search_param = "search"
    search_title = "Search products"
    search_description = "Search by product name, description, or SKU"


class ProductOrderingFilter(OrderingFilter):
    """
    Extended ordering filter for products.
    
    Allows ordering by:
        - price: Price (ascending/descending)
        - created_at: Creation date
        - name: Product name
        - stock_quantity: Stock level
    """
    ordering_param = "ordering"
    ordering_title = "Sort results"
    ordering_description = "Sort by price, created_at, name, or stock_quantity"

    def get_valid_fields(self, queryset, view, context):
        """Get list of valid ordering fields."""
        return [
            ("price", "Price"),
            ("-price", "Price (Highest)"),
            ("created_at", "Newest"),
            ("-created_at", "Oldest"),
            ("name", "Name (A-Z)"),
            ("-name", "Name (Z-A)"),
            ("stock_quantity", "Stock (Low to High)"),
            ("-stock_quantity", "Stock (High to Low)"),
        ]
