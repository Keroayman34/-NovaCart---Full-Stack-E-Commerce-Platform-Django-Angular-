from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation(order):
    """Send a simple order confirmation email to the order user.

    This helper intentionally uses Django's `send_mail` so the project can
    use the console backend during development or swap in a real backend
    in production via settings.
    """
    user = getattr(order, "user", None)
    if user is None:
        return

    recipient = getattr(user, "email", None)
    if not recipient:
        return

    subject = f"Order Confirmation — #{order.id}"

    lines = [
        f"Thank you for your order, {getattr(user, 'first_name', '')}!",
        "",
        f"Order ID: {order.id}",
        f"Placed: {order.created_at}",
        "",
        "Items:",
    ]

    for item in getattr(order, "items", []).all():
        prod = getattr(item, "product", None)
        name = getattr(prod, "name", str(prod)) if prod is not None else "Product"
        lines.append(f"- {name} x {item.quantity}: {item.price_at_purchase}")

    lines += ["", f"Total: {order.total_price}", "", "Estimated delivery: 3-7 business days."]

    message = "\n".join(lines)

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@novacart.local"),
        [recipient],
        fail_silently=True,
    )
