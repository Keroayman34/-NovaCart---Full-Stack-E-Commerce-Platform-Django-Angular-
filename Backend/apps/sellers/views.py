from decimal import Decimal

from django.db.models import Avg, F, Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from apps.orders.models import Order, OrderItem
from apps.products.serializers import ProductSerializer
from apps.products.models import Product

from .models import SellerProfile
from .serializers import *
from core.permissions import IsSeller


class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = [JSONParser, MultiPartParser, FormParser]


    def get(self, request):
        try:
            profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "No shop profile found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SellerProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateSellerProfileSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            profile = serializer.save()
            return Response(
                SellerProfileSerializer(profile, context={"request": request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "No shop profile found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CreateSellerProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                SellerProfileSerializer(profile, context={"request": request}).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SellerOwnerProductListView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
class SellerOwnerProductDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)
    

class SellerOwnerProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller ]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product, context={"request": request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SellerOwnerProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SellerOwnerProductDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, seller=request.user)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        seller = request.user

        seller_products = Product.objects.filter(seller=seller)
        active_products = seller_products.filter(is_active=True, is_deleted=False)

        seller_order_items = OrderItem.objects.filter(
            product__seller=seller
        ).select_related('order', 'product')

        seller_order_ids = seller_order_items.values_list('order_id', flat=True).distinct()
        seller_orders = Order.objects.filter(id__in=seller_order_ids).prefetch_related(
            'items__product'
        ).order_by('-created_at')

        delivered_items = seller_order_items.filter(order__status=Order.Status.DELIVERED)
        total_sales = Decimal('0.00')
        for item in delivered_items:
            total_sales += item.price * item.quantity

        total_orders = seller_orders.count()

        active_products_count = active_products.count()

        avg_rating = active_products.aggregate(
            avg=Avg('average_rating')
        )['avg'] or 0

        recent_orders_data = []
        for order in seller_orders[:5]:
            seller_items = [
                item for item in order.items.all()
                if item.product.seller_id == seller.id
            ]
            recent_orders_data.append({
                'id': order.id,
                'customer': order.user.email if order.user else 'N/A',
                'amount': float(order.total_price),
                'status': order.status,
                'date': order.created_at.isoformat(),
            })

        product_revenue = (
            seller_order_items
            .filter(order__status=Order.Status.DELIVERED)
            .values('product_id', 'product__name')
            .annotate(
                total_qty=Sum('quantity'),
                total_revenue=Sum(F('quantity') * F('price')),
            )
            .order_by('-total_revenue')[:5]
        )

        top_products_data = []
        for item in product_revenue:
            top_products_data.append({
                'name': item['product__name'],
                'sales': item['total_qty'],
                'revenue': float(item['total_revenue']),
            })

        return Response({
            'stats': [
                {
                    'label': 'Total Sales',
                    'value': str(total_sales),
                    'icon': '💰',
                    'trend': None,
                    'color': 'blue',
                },
                {
                    'label': 'Total Orders',
                    'value': total_orders,
                    'icon': '📦',
                    'trend': None,
                    'color': 'green',
                },
                {
                    'label': 'Active Products',
                    'value': active_products_count,
                    'icon': '📊',
                    'trend': None,
                    'color': 'purple',
                },
                {
                    'label': 'Avg Rating',
                    'value': round(float(avg_rating), 2),
                    'icon': '⭐',
                    'trend': None,
                    'color': 'orange',
                },
            ],
            'recentOrders': recent_orders_data,
            'topProducts': top_products_data,
        })