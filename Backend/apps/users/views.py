from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    EmailSerializer,
    ProfileSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
)
from .services import UserEmailService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserEmailService.send_verification_email(request, user)
            return Response({
                "message": "Account created successfully! Please check your inbox to verify your email address.",
                "user": ProfileSerializer(user, context={"request": request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_verified:
            return Response({"message": "Email is already verified."})
        UserEmailService.send_verification_email(request, request.user)
        return Response({"message": "Verification email sent."})


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = VerifyEmailSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=["is_verified", "is_active"])
        return Response({"message": "Email verified successfully."})

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=["is_verified", "is_active"])
        return Response({"message": "Email verified successfully."})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data["email"], is_active=True).first()
        if user:
            UserEmailService.send_password_reset_email(request, user)
        return Response({"message": "If the email exists, a reset link has been sent."})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"message": "Password reset successfully."})
