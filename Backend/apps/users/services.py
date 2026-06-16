from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import email_verification_token


class UserEmailService:
    @staticmethod
    def build_absolute_url(request, path, query):
        base_url = getattr(settings, "FRONTEND_URL", "") or request.build_absolute_uri("/")[:-1]
        separator = "&" if "?" in path else "?"
        return f"{base_url}{path}{separator}{query}"

    @staticmethod
    def send_verification_email(request, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)
        api_path = reverse("verify-email")
        api_url = request.build_absolute_uri(f"{api_path}?uid={uid}&token={token}")
        frontend_url = UserEmailService.build_absolute_url(
            request,
            "/auth/verify-email",
            f"uid={uid}&token={token}",
        )
        send_mail(
            "Verify your NovaCart email",
            f"Verify your email using this link: {frontend_url}\nAPI link: {api_url}",
            getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@novacart.local"),
            [user.email],
            fail_silently=False,
        )
        return {"uid": uid, "token": token}

    @staticmethod
    def send_password_reset_email(request, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = UserEmailService.build_absolute_url(
            request,
            "/auth/reset-password",
            f"uid={uid}&token={token}",
        )
        send_mail(
            "Reset your NovaCart password",
            f"Reset your password using this link: {frontend_url}",
            getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@novacart.local"),
            [user.email],
            fail_silently=False,
        )
        return {"uid": uid, "token": token}
