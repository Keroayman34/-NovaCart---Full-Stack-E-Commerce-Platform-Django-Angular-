from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistAddRemoveSerializer
from apps.products.models import Product


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get_wishlist(self, user):
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        return wishlist

    def get(self, request):
        wishlist = self.get_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistAddRemoveSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = self.get_wishlist(request.user)
            product = Product.objects.get(id=serializer.validated_data['product_id'])
            wishlist.products.add(product)
            return Response({"message": "المنتج اتضاف للـ wishlist."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = WishlistAddRemoveSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = self.get_wishlist(request.user)
            product = Product.objects.get(id=serializer.validated_data['product_id'])
            wishlist.products.remove(product)
            return Response({"message": "المنتج اتحذف من الـ wishlist."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)