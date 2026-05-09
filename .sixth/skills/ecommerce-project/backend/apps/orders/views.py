from decimal import Decimal

from django.apps import apps
from django.db import transaction
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .permissions import CanUpdateOrderStatus


def _get_cart_item_model():
	return apps.get_model("cart", "CartItem")


def _get_product_price(product):
	for attribute_name in ("price", "current_price", "sale_price"):
		price_value = getattr(product, attribute_name, None)
		if price_value is not None:
			return Decimal(str(price_value))
	raise serializers.ValidationError("Product price is not available.")


def _get_product_stock_field(product):
	for attribute_name in ("stock", "quantity_in_stock", "available_stock"):
		if hasattr(product, attribute_name):
			return attribute_name
	return None


class PlaceOrderView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = OrderSerializer

	def post(self, request, *args, **kwargs):
		cart_item_model = _get_cart_item_model()
		cart_items = list(
			cart_item_model.objects.select_related("product").filter(user=request.user)
		)

		if not cart_items:
			raise serializers.ValidationError("Your cart is empty.")

		with transaction.atomic():
			order = Order.objects.create(user=request.user, status=Order.Status.PENDING)
			total_price = Decimal("0.00")

			for cart_item in cart_items:
				product = cart_item.product
				stock_field = _get_product_stock_field(product)
				if stock_field is None:
					raise serializers.ValidationError("Product stock is not available.")

				available_stock = getattr(product, stock_field)
				if available_stock < cart_item.quantity:
					raise serializers.ValidationError(
						f"Product '{product}' is out of stock."
					)

				unit_price = _get_product_price(product)
				line_total = unit_price * cart_item.quantity
				total_price += line_total

				OrderItem.objects.create(
					order=order,
					product=product,
					quantity=cart_item.quantity,
					price_at_purchase=unit_price,
				)

				setattr(product, stock_field, available_stock - cart_item.quantity)
				product.save(update_fields=[stock_field])

			order.total_price = total_price
			order.save(update_fields=["total_price"])
			cart_item_model.objects.filter(user=request.user).delete()

		serializer = self.get_serializer(order)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateSerializer(serializers.Serializer):
	status = serializers.ChoiceField(choices=Order.Status.choices)


class OrderStatusUpdateView(generics.UpdateAPIView):
	queryset = Order.objects.prefetch_related("items__product")
	serializer_class = OrderStatusUpdateSerializer
	permission_classes = [permissions.IsAuthenticated, CanUpdateOrderStatus]

	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	def partial_update(self, request, *args, **kwargs):
		order = self.get_object()
		self.check_object_permissions(request, order)

		serializer = self.get_serializer(order, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)

		order.status = serializer.validated_data["status"]
		order.save(update_fields=["status"])

		return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
