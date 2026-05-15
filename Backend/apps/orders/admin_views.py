from django.apps import apps
from rest_framework import generics, serializers
from rest_framework.response import Response

from core.permissions import IsAdminUser


def _get_order_model():
	return apps.get_model("orders", "Order")


class AdminOrderReadSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	user = serializers.IntegerField(read_only=True, required=False)
	status = serializers.CharField(read_only=True, required=False)
	created_at = serializers.DateTimeField(read_only=True, required=False)
	total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, required=False)

	def to_representation(self, instance):
		return {
			"id": instance.pk,
			"user": getattr(instance, "user_id", None),
			"status": getattr(instance, "status", None),
			"created_at": getattr(instance, "created_at", None),
			"total_price": getattr(instance, "total_price", None),
		}


class AdminOrderListView(generics.ListAPIView):
	permission_classes = [IsAdminUser]
	serializer_class = AdminOrderReadSerializer

	def get_queryset(self):
		Order = _get_order_model()
		queryset = Order.objects.all().order_by("-id")

		status_param = self.request.query_params.get("status")
		if status_param and hasattr(Order, "status"):
			queryset = queryset.filter(status=status_param)

		date_param = self.request.query_params.get("date")
		if date_param and hasattr(Order, "created_at"):
			queryset = queryset.filter(created_at__date=date_param)

		return queryset


class AdminOrderUpdateView(generics.GenericAPIView):
	permission_classes = [IsAdminUser]

	def get_queryset(self):
		Order = _get_order_model()
		return Order.objects.all()

	def patch(self, request, *args, **kwargs):
		order = self.get_queryset().filter(pk=kwargs.get("pk")).first()
		if not order:
			raise serializers.ValidationError("Order not found.")

		model_fields = {
			field.name
			for field in order._meta.fields
			if field.name not in {"id", "pk", "created_at"}
		}

		incoming = request.data or {}
		unknown = [key for key in incoming.keys() if key not in model_fields]
		if unknown:
			raise serializers.ValidationError({"detail": f"Unknown field(s): {', '.join(unknown)}"})

		update_fields = []
		for key, value in incoming.items():
			setattr(order, key, value)
			update_fields.append(key)

		if update_fields:
			order.save(update_fields=update_fields)

		return Response(AdminOrderReadSerializer(order).data)
