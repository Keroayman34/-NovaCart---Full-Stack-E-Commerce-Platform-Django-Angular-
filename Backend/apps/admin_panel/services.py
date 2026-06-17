from django.utils import timezone


class UserManagementService:

    @staticmethod
    def approve_user(user):
        user.status = "approved"
        user.save(update_fields=["status"])

    @staticmethod
    def restrict_user(user):
        user.status = "restricted"
        user.save(update_fields=["status"])

    @staticmethod
    def soft_delete(user):
        user.is_deleted = True
        user.deleted_at = timezone.now()

        user.save(
            update_fields=[
                "is_deleted",
                "deleted_at"
            ]
        )