from rest_framework import serializers

from apps.products.models import Product

from .models import Wishlist


from apps.products.serializers import ProductImageSerializer

class ProductBriefSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'primary_image']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image, context=self.context).data
        return None


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
