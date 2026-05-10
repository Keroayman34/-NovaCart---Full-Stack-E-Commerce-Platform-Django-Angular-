"""
Product and Category models for the e-commerce platform.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

User = get_user_model()


class Category(models.Model):
    """
    Product category model.
    
    Attributes:
        name: Category name (unique)
        slug: URL-friendly identifier (auto-generated)
        description: Category description
        image: Category image/icon
        is_active: Soft-delete flag
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Category name"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False,
        help_text="URL-friendly identifier"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Category description"
    )
    image = models.ImageField(
        upload_to="categories/%Y/%m/",
        blank=True,
        null=True,
        help_text="Category image/icon"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Is category active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "-created_at"]),
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate category data."""
        # Check for duplicate names (case-insensitive)
        if Category.objects.filter(
            name__iexact=self.name
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"name": "A category with this name already exists."}
            )


class Product(models.Model):
    """
    Product model.
    
    Attributes:
        category: ForeignKey to Category
        seller: ForeignKey to User (seller)
        name: Product name
        slug: URL-friendly identifier (auto-generated)
        description: Product description
        sku: Stock Keeping Unit (unique)
        price: Product price
        stock_quantity: Available stock
        is_active: Product visibility flag
        is_deleted: Soft-delete flag
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        help_text="Product category"
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"role": "seller"},
        help_text="Product seller"
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Product name"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False,
        help_text="URL-friendly identifier"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Product description"
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Stock Keeping Unit"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product price"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Available stock quantity"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Is product visible to customers"
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft delete flag"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp"
    )

    objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["seller", "is_deleted"]),
            models.Index(fields=["is_active", "is_deleted", "-created_at"]),
            models.Index(fields=["category", "is_active", "is_deleted"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["sku"],
                name="unique_sku_constraint",
                condition=models.Q(is_deleted=False),
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate product data."""
        errors = {}

        # Validate price
        if self.price <= 0:
            errors["price"] = "Price must be greater than 0."

        # Validate stock quantity
        if self.stock_quantity < 0:
            errors["stock_quantity"] = "Stock quantity cannot be negative."

        # Validate category
        if not self.category_id:
            errors["category"] = "Category is required."

        # Check for duplicate SKU
        if Product.objects.filter(
            sku=self.sku,
            is_deleted=False
        ).exclude(pk=self.pk).exists():
            errors["sku"] = "This SKU is already in use by another product."

        # Check for duplicate slug
        if Product.objects.filter(
            slug=self.slug
        ).exclude(pk=self.pk).exists():
            errors["slug"] = "This slug is already taken."

        if errors:
            raise ValidationError(errors)

    def soft_delete(self):
        """Soft delete the product."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        """Restore a soft-deleted product."""
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0


class ProductImage(models.Model):
    """
    Product image model.
    
    Attributes:
        product: ForeignKey to Product
        image: Image file
        is_primary: Primary image flag
        alt_text: Alternative text for accessibility
        created_at: Creation timestamp
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Associated product"
    )
    image = models.ImageField(
        upload_to="products/%Y/%m/",
        help_text="Product image"
    )
    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Is this the primary image"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Alternative text for accessibility"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp"
    )

    class Meta:
        ordering = ["-is_primary", "created_at"]
        indexes = [
            models.Index(fields=["product", "is_primary"]),
        ]
        unique_together = [
            ["product", "image"]
        ]

    def __str__(self):
        return f"Image for {self.product.name}"

    def clean(self):
        """Validate image data."""
        if self.is_primary:
            # Check if another primary image exists for this product
            if ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "This product already has a primary image. "
                    "Please unset the other primary image first."
                )

    def save(self, *args, **kwargs):
        """Save image and ensure only one primary image per product."""
        self.clean()
        
        # If this is being set as primary, unset others
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        
        super().save(*args, **kwargs)
