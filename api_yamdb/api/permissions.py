from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Права доступа для админа."""
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        return False
