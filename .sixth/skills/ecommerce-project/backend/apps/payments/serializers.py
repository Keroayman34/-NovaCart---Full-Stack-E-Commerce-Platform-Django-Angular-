from django.utils import timezone
from rest_framework import serializers

from apps.orders.models import Order

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
	order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

	class Meta:
		model = Payment
		fields = ["id", "order", "method", "status", "transaction_id", "paid_at", "created_at"]
		read_only_fields = ["id", "status", "transaction_id", "paid_at", "created_at"]

	def validate_order(self, order):
		request = self.context.get("request")
		if request and order.user_id != request.user.id:
			raise serializers.ValidationError("You can only pay for your own order.")
		if hasattr(order, "payment"):
			raise serializers.ValidationError("Payment already exists for this order.")
		return order

	def create(self, validated_data):
		order = validated_data["order"]
		payment = Payment.objects.create(
			order=order,
			method=validated_data["method"],
			status=Payment.Status.PAID,
			transaction_id=f"MOCK-{order.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
			paid_at=timezone.now(),
		)
		return payment
