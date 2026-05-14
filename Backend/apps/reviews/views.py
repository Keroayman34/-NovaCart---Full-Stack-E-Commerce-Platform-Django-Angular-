from django.apps import apps
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from .models import Review
from .serializers import ReviewSerializer


class ProductReviewListCreateView(generics.ListCreateAPIView):
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def _get_product(self):
		Product = apps.get_model("products", "Product")
		product = Product.objects.filter(pk=self.kwargs["product_id"]).first()
		if not product:
			raise NotFound("Product not found.")
		return product

	def get_queryset(self):
		product = self._get_product()
		return Review.objects.filter(product=product).select_related("user", "product")

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context["product"] = self._get_product()
		return context

	def perform_create(self, serializer):
		serializer.save(user=self.request.user, product=self._get_product())
