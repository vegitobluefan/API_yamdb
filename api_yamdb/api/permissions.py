from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права доступа для админа."""
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        return False


class AdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Автор, админ, модератор. В остальных случаях только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )


class AdminOrSuperuserOrReadOnly(permissions.BasePermission):
    """Администратор или суперюзер. В остальных случаях только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )
