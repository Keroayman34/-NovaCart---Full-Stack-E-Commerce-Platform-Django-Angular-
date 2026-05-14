from django.apps import apps
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Wishlist
from .serializers import WishlistSerializer, WishlistAddSerializer


class WishlistListView(generics.ListAPIView):
	serializer_class = WishlistSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Wishlist.objects.filter(user=self.request.user).select_related("product")


class WishlistAddView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = WishlistAddSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		Product = apps.get_model("products", "Product")
		product = Product.objects.filter(id=serializer.validated_data["product_id"]).first()
		if not product:
			return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

		if Wishlist.objects.filter(user=request.user, product=product).exists():
			return Response({"error": "Product is already in your wishlist."}, status=status.HTTP_400_BAD_REQUEST)

		wishlist_item = Wishlist.objects.create(user=request.user, product=product)
		return Response(WishlistSerializer(wishlist_item).data, status=status.HTTP_201_CREATED)


class WishlistRemoveView(generics.DestroyAPIView):
	queryset = Wishlist.objects.all()
	serializer_class = WishlistSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_field = "pk"

	def get_queryset(self):
		return Wishlist.objects.filter(user=self.request.user)
