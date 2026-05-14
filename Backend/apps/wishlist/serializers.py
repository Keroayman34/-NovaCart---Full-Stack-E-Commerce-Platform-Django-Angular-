from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wishlist
		fields = ["id", "user", "product", "added_at"]
		read_only_fields = ["id", "user", "added_at"]

	def validate(self, attrs):
		request = self.context.get("request")
		product = attrs.get("product")

		if request and request.method == "POST" and product is not None:
			already_exists = Wishlist.objects.filter(user=request.user, product=product).exists()
			if already_exists:
				raise serializers.ValidationError("Product is already in your wishlist.")

		return attrs


class WishlistAddSerializer(serializers.Serializer):
	product_id = serializers.IntegerField()
