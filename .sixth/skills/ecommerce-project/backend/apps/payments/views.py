from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentCreateView(generics.CreateAPIView):
	queryset = Payment.objects.select_related("order", "order__user")
	serializer_class = PaymentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		payment = serializer.save()
		return Response(PaymentSerializer(payment, context=self.get_serializer_context()).data, status=status.HTTP_201_CREATED)
