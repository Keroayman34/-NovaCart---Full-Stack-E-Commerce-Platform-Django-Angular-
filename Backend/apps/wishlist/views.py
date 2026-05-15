from django.apps import apps
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wishlist
from .serializers import ProductBriefSerializer, WishlistAddRemoveSerializer


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get_wishlist(self, user):
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        return wishlist

    def get(self, request):
        wishlist = self.get_wishlist(request.user)
        serializer = ProductBriefSerializer(wishlist.products.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistAddRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wishlist = self.get_wishlist(request.user)
        Product = apps.get_model('products', 'Product')
        product = Product.objects.filter(id=serializer.validated_data['product_id']).first()
        if not product:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist.products.add(product)
        return Response({'message': 'المنتج اتضاف للـ wishlist.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id=None):
        serializer = WishlistAddRemoveSerializer(data={'product_id': product_id or request.data.get('product_id')})
        serializer.is_valid(raise_exception=True)

        wishlist = self.get_wishlist(request.user)
        Product = apps.get_model('products', 'Product')
        product = Product.objects.filter(id=serializer.validated_data['product_id']).first()
        if not product:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist.products.remove(product)
        return Response({'message': 'المنتج اتحذف من الـ wishlist.'}, status=status.HTTP_200_OK)
