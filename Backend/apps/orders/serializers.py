from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from apps.cart.models import Cart

from .models import Order, OrderItem


def _get_product_stock_field(product):
    for attribute_name in ('stock', 'quantity_in_stock', 'stock_quantity', 'available_stock'):
        if hasattr(product, attribute_name):
            return attribute_name
    return None


def _get_product_price(product):
    for attribute_name in ('price', 'current_price', 'sale_price'):
        price_value = getattr(product, attribute_name, None)
        if price_value is not None:
            return Decimal(str(price_value))
    raise serializers.ValidationError('Product price is not available.')


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
        request = self.context['request']
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = list(cart.items.select_related('product'))

        if not cart_items:
            raise serializers.ValidationError('Your cart is empty.')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                address=validated_data['address'],
                status=Order.Status.PENDING,
            )
            total_price = Decimal('0.00')

            for cart_item in cart_items:
                product = cart_item.product
                stock_field = _get_product_stock_field(product)
                if stock_field is not None:
                    available_stock = getattr(product, stock_field)
                    if available_stock < cart_item.quantity:
                        raise serializers.ValidationError(f"Product '{product}' is out of stock.")
                    setattr(product, stock_field, available_stock - cart_item.quantity)
                    product.save(update_fields=[stock_field])

                unit_price = _get_product_price(product)
                total_price += unit_price * cart_item.quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item.quantity,
                    price=unit_price,
                )

            order.total_price = total_price
            order.save(update_fields=['total_price'])
            cart.items.all().delete()

        return order
