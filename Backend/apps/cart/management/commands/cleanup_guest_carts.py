"""Management command to delete inactive guest carts."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.cart.models import Cart


class Command(BaseCommand):
    """Delete guest carts inactive for 7+ days."""

    help = "Delete inactive guest carts (7+ days old)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Number of days of inactivity before deletion (default: 7)",
        )

    def handle(self, *args, **options):
        days = options["days"]
        cutoff_date = timezone.now() - timedelta(days=days)

        deleted_count, _ = Cart.objects.filter(
            user_id=None,
            session_key__isnull=False,
            updated_at__lt=cutoff_date,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_count} inactive guest carts "
                f"(inactive for {days}+ days)"
            )
        )
