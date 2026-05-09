from django.conf import settings
from django.db import models


class Payment(models.Model):
	class Method(models.TextChoices):
		CARD = "card", "Card"
		PAYPAL = "paypal", "Paypal"
		CASH = "cash", "Cash"
		WALLET = "wallet", "Wallet"

	class Status(models.TextChoices):
		PAID = "paid", "Paid"
		PENDING = "pending", "Pending"
		FAILED = "failed", "Failed"

	order = models.OneToOneField(
		"orders.Order",
		on_delete=models.CASCADE,
		related_name="payment",
	)
	method = models.CharField(max_length=20, choices=Method.choices)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	transaction_id = models.CharField(max_length=120, blank=True)
	paid_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Payment #{self.pk} - {self.order_id}"
