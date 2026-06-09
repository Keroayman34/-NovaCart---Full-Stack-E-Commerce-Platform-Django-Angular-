from django.conf import settings
from django.db import models
from django.db.models import Avg, Count
from apps.products.models import Product


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.product.name} - {self.rating}/5'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_product_rating_summary()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        self._update_product_rating_summary(product=product)

    def _update_product_rating_summary(self, product=None):
        product = product or self.product
        agg = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'), total=Count('id'))

        update_fields = []
        avg_rating = agg['avg_rating'] or 0
        total_reviews = agg['total'] or 0

        for field_name in ('average_rating', 'avg_rating', 'rating'):
            if hasattr(product, field_name):
                setattr(product, field_name, avg_rating)
                update_fields.append(field_name)
                break

        for field_name in ('rating_count', 'reviews_count', 'total_reviews'):
            if hasattr(product, field_name):
                setattr(product, field_name, total_reviews)
                update_fields.append(field_name)
                break

        if update_fields:
            product.save(update_fields=update_fields)
