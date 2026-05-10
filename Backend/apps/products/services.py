"""
Service layer for Product and Category business logic.

This module contains all business logic operations related to products and categories.
Views should delegate to these services instead of implementing logic directly.
"""
from django.utils.text import slugify
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Product, Category, ProductImage


class CategoryService:
    """Service for category-related operations."""

    @staticmethod
    def create_category(name, description=None, image=None):
        """
        Create a new category.
        
        Args:
            name: Category name
            description: Category description
            image: Category image
            
        Returns:
            Created Category instance
            
        Raises:
            ValidationError: If category data is invalid
        """
        category = Category(
            name=name,
            description=description,
            image=image,
        )
        category.full_clean()
        category.save()
        return category

    @staticmethod
    def update_category(category, **kwargs):
        """
        Update a category.
        
        Args:
            category: Category instance
            **kwargs: Fields to update
            
        Returns:
            Updated Category instance
        """
        for field, value in kwargs.items():
            if hasattr(category, field):
                setattr(category, field, value)
        category.full_clean()
        category.save()
        return category

    @staticmethod
    def delete_category(category):
        """
        Soft delete a category by marking it inactive.
        
        Args:
            category: Category instance
        """
        category.is_active = False
        category.save(update_fields=["is_active"])

    @staticmethod
    def activate_category(category):
        """
        Activate a category.
        
        Args:
            category: Category instance
        """
        category.is_active = True
        category.save(update_fields=["is_active"])


class ProductService:
    """Service for product-related operations."""

    @staticmethod
    def generate_slug(name, instance=None):
        """
        Generate a unique slug from product name.
        
        Args:
            name: Product name
            instance: Product instance (for update operations)
            
        Returns:
            Unique slug string
        """
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        # Check for existing products with the same slug
        query = Product.objects.filter(slug=slug)
        if instance:
            query = query.exclude(pk=instance.pk)

        while query.exists():
            slug = f"{base_slug}-{counter}"
            query = Product.objects.filter(slug=slug)
            if instance:
                query = query.exclude(pk=instance.pk)
            counter += 1

        return slug

    @staticmethod
    @transaction.atomic
    def create_product(category, seller, name, sku, price, stock_quantity,
                       description=None, is_active=True):
        """
        Create a new product with validation.
        
        Args:
            category: Category instance
            seller: Seller (User instance)
            name: Product name
            sku: Stock Keeping Unit
            price: Product price
            stock_quantity: Initial stock quantity
            description: Product description
            is_active: Product visibility flag
            
        Returns:
            Created Product instance
            
        Raises:
            ValidationError: If product data is invalid
        """
        product = Product(
            category=category,
            seller=seller,
            name=name,
            sku=sku,
            price=price,
            stock_quantity=stock_quantity,
            description=description,
            is_active=is_active,
        )
        product.full_clean()
        product.save()
        return product

    @staticmethod
    def update_product(product, **kwargs):
        """
        Update a product.
        
        Args:
            product: Product instance
            **kwargs: Fields to update
            
        Returns:
            Updated Product instance
        """
        # Don't allow updating seller
        kwargs.pop("seller", None)

        for field, value in kwargs.items():
            if hasattr(product, field) and field != "seller":
                setattr(product, field, value)

        product.full_clean()
        product.save()
        return product

    @staticmethod
    def soft_delete_product(product):
        """
        Soft delete a product.
        
        Args:
            product: Product instance
        """
        product.soft_delete()

    @staticmethod
    def restore_product(product):
        """
        Restore a soft-deleted product.
        
        Args:
            product: Product instance
        """
        product.restore()

    @staticmethod
    def update_stock(product, quantity_change):
        """
        Update product stock quantity.
        
        Args:
            product: Product instance
            quantity_change: Amount to change (positive or negative)
            
        Raises:
            ValidationError: If resulting stock would be negative
        """
        new_quantity = product.stock_quantity + quantity_change

        if new_quantity < 0:
            raise ValidationError(
                f"Cannot reduce stock below 0. Current stock: {product.stock_quantity}"
            )

        product.stock_quantity = new_quantity
        product.save(update_fields=["stock_quantity"])

    @staticmethod
    def deactivate_product(product):
        """
        Deactivate (hide) a product.
        
        Args:
            product: Product instance
        """
        product.is_active = False
        product.save(update_fields=["is_active"])

    @staticmethod
    def activate_product(product):
        """
        Activate (show) a product.
        
        Args:
            product: Product instance
        """
        product.is_active = True
        product.save(update_fields=["is_active"])


class ProductImageService:
    """Service for product image operations."""

    @staticmethod
    @transaction.atomic
    def add_image(product, image, is_primary=False, alt_text=None):
        """
        Add an image to a product.
        
        Args:
            product: Product instance
            image: Image file
            is_primary: Whether to set as primary image
            alt_text: Alternative text
            
        Returns:
            Created ProductImage instance
        """
        product_image = ProductImage(
            product=product,
            image=image,
            is_primary=is_primary,
            alt_text=alt_text,
        )
        product_image.full_clean()
        product_image.save()
        return product_image

    @staticmethod
    def remove_image(product_image):
        """
        Remove an image from a product.
        
        Args:
            product_image: ProductImage instance
        """
        product_image.delete()

    @staticmethod
    def set_primary_image(product, product_image):
        """
        Set a specific image as primary for a product.
        
        Args:
            product: Product instance
            product_image: ProductImage instance to set as primary
            
        Raises:
            ValidationError: If image doesn't belong to product
        """
        if product_image.product_id != product.id:
            raise ValidationError(
                "The image does not belong to this product."
            )

        # Unset all other primary images
        ProductImage.objects.filter(
            product=product,
            is_primary=True
        ).update(is_primary=False)

        # Set this image as primary
        product_image.is_primary = True
        product_image.save(update_fields=["is_primary"])

    @staticmethod
    def get_primary_image(product):
        """
        Get the primary image of a product.
        
        Args:
            product: Product instance
            
        Returns:
            ProductImage instance or None
        """
        return product.images.filter(is_primary=True).first()
