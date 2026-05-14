from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ["id", "user", "product", "rating", "comment", "created_at"]
		read_only_fields = ["id", "user", "product", "created_at"]

	def validate_rating(self, value):
		if value < 1 or value > 5:
			raise serializers.ValidationError("Rating must be between 1 and 5.")
		return value

	def validate(self, attrs):
		request = self.context.get("request")
		product = self.context.get("product")

		if request and request.method == "POST" and product is not None:
			already_exists = Review.objects.filter(user=request.user, product=product).exists()
			if already_exists:
				raise serializers.ValidationError("You have already reviewed this product.")

		return attrs
