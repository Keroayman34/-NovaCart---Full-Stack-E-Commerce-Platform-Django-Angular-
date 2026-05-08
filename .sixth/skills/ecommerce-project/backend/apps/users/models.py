from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	class Roles(models.TextChoices):
		CUSTOMER = "customer", "Customer"
		SELLER = "seller", "Seller"
		ADMIN = "admin", "Admin"

	email = models.EmailField(unique=True)
	role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)
	is_verified = models.BooleanField(default=False)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]

	def __str__(self) -> str:
		return self.email
