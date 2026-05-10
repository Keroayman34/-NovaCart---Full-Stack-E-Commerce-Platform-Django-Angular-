"""
Django app configuration for products app.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration class for the products app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = "Products"

    def ready(self):
        """Import signals when app is ready."""
        # Import signals here if needed
        pass
