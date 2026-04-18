from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminUser(IsAdminUser):
    """
    Only allow access to admin/superuser users.
    """
    message = 'Only administrators can access this resource.'
