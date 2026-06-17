from django.urls import path
from .views import (
    ChangePasswordView,
    CustomTokenObtainPairView,
    ForgotPasswordView,
    ProfileView,
    RegisterView,
    ResetPasswordView,
    SendVerificationEmailView,
    VerifyEmailView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    path('auth/send-verification/', SendVerificationEmailView.as_view(), name='send-verification'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
