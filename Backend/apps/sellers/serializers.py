from rest_framework import serializers
from .models import SellerProfile
from apps.users.serializers import ProfileSerializer
from apps.products.serializers import ProductSerializer


class SellerProfileSerializer(serializers.ModelSerializer):

    user = ProfileSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'shop_name', 'shop_description', 'shop_logo', 'address', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CreateSellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProfile
        fields = ['shop_name', 'shop_description', 'shop_logo', 'address']

    def validate(self, attrs):
        user = self.context['request'].user

        if user.role != 'seller':
            raise serializers.ValidationError("Only sellers can create a shop profile.")

        if SellerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("You already have a shop profile.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return SellerProfile.objects.create(user=user, **validated_data)
    

class SellerProductOwnerListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SellerProfile
        fields = ['id', 'shop_name', 'products']
        read_only_fields = ['id', 'shop_name', 'products']


class SellerProductOwnerDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SellerProfile
        fields = ['id', 'shop_name', 'shop_description', 'shop_logo', 'address', 'products']
        read_only_fields = ['id', 'shop_name', 'shop_description', 'shop_logo', 'address', 'products']

    
class SellerProductOwnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['shop_name', 'shop_description', 'shop_logo', 'address']

    def validate(self, attrs):
        user = self.context['request'].user

        if user.role != 'seller':
            raise serializers.ValidationError("Only sellers can create a shop profile.")

        if SellerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("You already have a shop profile.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return SellerProfile.objects.create(user=user, **validated_data)
    
