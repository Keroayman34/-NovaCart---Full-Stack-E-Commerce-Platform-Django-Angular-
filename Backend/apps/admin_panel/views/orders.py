from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from core.permissions import IsAdmin


class AdminOrderListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)    

class AdminOrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = AdminUpdateStatusSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_status = serializer.validated_data['status']
            order.status = new_status
            order.save()
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

class AdminCancelOrderView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.status in ['shipped', 'delivered']:
                return Response({'error': 'Cannot cancel shipped or delivered orders'}, status=status.HTTP_400_BAD_REQUEST)
            order.status = 'cancelled'
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)