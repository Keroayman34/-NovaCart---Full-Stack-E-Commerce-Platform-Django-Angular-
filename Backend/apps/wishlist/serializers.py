from rest_framework import serializers

from apps.products.models import Product

from .models import Wishlist


class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'created_at']


class WishlistAddRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('المنتج مش موجود.')
        return value
