from django.conf import settings
from django.db import models


class Wishlist(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="wishlist_items",
	)
	product = models.ForeignKey(
		"products.Product",
		on_delete=models.CASCADE,
		related_name="wishlist_entries",
	)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-added_at"]
		constraints = [
			models.UniqueConstraint(fields=["user", "product"], name="unique_wishlist_per_user_product"),
		]

	def __str__(self):
		return f"Wishlist item #{self.pk} - {self.user}"
