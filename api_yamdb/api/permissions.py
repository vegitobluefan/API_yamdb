from rest_framework import permissions


class AdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Автор, админ, модератор. В остальных случаях только чтение."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user == obj.author or
            request.user.is_admin or
            request.user.is_moderator
        )


class AdminOrSuperuserOrReadOnly(permissions.BasePermission):
    """Администратор или суперюзер. В остальных случаях только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_admin)
        )
