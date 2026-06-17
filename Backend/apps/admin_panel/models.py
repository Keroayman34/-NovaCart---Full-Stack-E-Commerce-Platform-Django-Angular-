from django_db import models


class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Main title of the banner")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="Subtitle of the banner")
    image = models.ImageField(upload_to='banners/', help_text="Image for the banner")
    link_url = models.URLField(blank=True, null=True, help_text="Optional URL to link the banner to")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of the banner in the carousel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title if self.title else f"Banner {self.pk}"
    


