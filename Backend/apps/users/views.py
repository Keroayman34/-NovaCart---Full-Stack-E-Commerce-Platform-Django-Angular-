from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		data = UserSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]

		self._merge_guest_cart_if_exists(request, user)

		refresh = RefreshToken.for_user(user)
		return Response(
			{
				"access": str(refresh.access_token),
				"refresh": str(refresh),
				"user": UserSerializer(user).data,
			},
			status=status.HTTP_200_OK,
		)

	def _merge_guest_cart_if_exists(self, request, user):
		"""Merge guest cart into user cart after successful login."""
		from apps.cart.models import Cart
		from apps.cart.services import CartService

		session_key = request.session.session_key
		if not session_key:
			return

		guest_cart = Cart.objects.filter(
			session_key=session_key,
			user_id=None,
		).first()

		if not guest_cart:
			return

		user_cart, _ = Cart.objects.get_or_create(user=user, defaults={})

		try:
			CartService.merge_cart(guest_cart=guest_cart, user_cart=user_cart)
		except Exception:
			pass

