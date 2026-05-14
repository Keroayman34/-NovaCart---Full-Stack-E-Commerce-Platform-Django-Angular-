from decimal import Decimal

from django.apps import apps
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework import serializers
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from .stripe_utils import create_payment_intent, retrieve_payment_intent


class PaymentCreateView(generics.CreateAPIView):
	queryset = Payment.objects.select_related("order", "order__user")
	serializer_class = PaymentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		payment = serializer.save()
		return Response(PaymentSerializer(payment, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)


class StripePaymentIntentSerializer(serializers.Serializer):
	order_id = serializers.IntegerField()
	currency = serializers.CharField(default="usd")


class StripeConfirmSerializer(serializers.Serializer):
	payment_intent_id = serializers.CharField()
	order_id = serializers.IntegerField(required=False)


class StripePaymentIntentCreateView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StripePaymentIntentSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		Order = apps.get_model("orders", "Order")
		order = Order.objects.filter(id=serializer.validated_data["order_id"]).first()
		if not order:
			raise serializers.ValidationError("Order not found.")
		if order.user_id != request.user.id:
			raise serializers.ValidationError("You can only pay for your own order.")

		intent = create_payment_intent(
			amount=Decimal(str(order.total_price)),
			currency=serializer.validated_data["currency"],
			metadata={"order_id": str(order.id), "user_id": str(request.user.id)},
		)

		payment, _ = Payment.objects.get_or_create(
			order=order,
			defaults={
				"method": Payment.Method.CARD,
				"status": Payment.Status.PENDING,
				"transaction_id": intent.id,
			},
		)

		if payment.transaction_id != intent.id or payment.status != Payment.Status.PENDING:
			payment.method = Payment.Method.CARD
			payment.status = Payment.Status.PENDING
			payment.transaction_id = intent.id
			payment.paid_at = None
			payment.save(update_fields=["method", "status", "transaction_id", "paid_at"])

		return Response(
			{
				"order_id": order.id,
				"payment_intent_id": intent.id,
				"client_secret": intent.client_secret,
			},
			status=status.HTTP_200_OK,
		)


class StripePaymentConfirmView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StripeConfirmSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		payment_intent_id = serializer.validated_data["payment_intent_id"]
		intent = retrieve_payment_intent(payment_intent_id)

		order_id = serializer.validated_data.get("order_id")
		payment = Payment.objects.select_related("order").filter(transaction_id=payment_intent_id).first()
		if order_id and payment is None:
			payment = Payment.objects.select_related("order").filter(order_id=order_id).first()

		if payment is None:
			raise serializers.ValidationError("Payment record not found.")

		if payment.order.user_id != request.user.id:
			raise serializers.ValidationError("You can only confirm your own payment.")

		if intent.status == "succeeded":
			payment.status = Payment.Status.PAID
			payment.paid_at = timezone.now()
			payment.transaction_id = intent.id
			payment.save(update_fields=["status", "paid_at", "transaction_id"])
		else:
			payment.status = Payment.Status.FAILED
			payment.transaction_id = intent.id
			payment.save(update_fields=["status", "transaction_id"])

		return Response(
			{
				"payment_id": payment.id,
				"order_id": payment.order_id,
				"status": payment.status,
				"transaction_id": payment.transaction_id,
			},
			status=status.HTTP_200_OK,
		)
