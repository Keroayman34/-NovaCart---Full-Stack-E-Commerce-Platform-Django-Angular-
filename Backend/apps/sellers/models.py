from django.db import models
from django.conf import settings


class SellerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )

    shop_name = models.CharField(max_length=100)

    shop_description = models.TextField(blank=True)

    shop_logo = models.ImageField(
        upload_to="shops/logos/",
        blank=True,
        null=True
    )

    address = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shop_name} ({self.user.email})"