from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total']
        read_only_fields = ['price']

    def get_total(self, obj):
        return obj.get_total()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'address', 'items', 'created_at']
        read_only_fields = ['user', 'status', 'total_price']


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['address']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart

        if not cart.items.exists():
            raise serializers.ValidationError("السلة فاضية.")

        order = Order.objects.create(
            user=user,
            address=validated_data['address'],
        )

        total = 0
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
            total += cart_item.product.price * cart_item.quantity

        order.total_price = total
        order.save()

        cart.items.all().delete()

        return order