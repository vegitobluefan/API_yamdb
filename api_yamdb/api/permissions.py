from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.method in SAFE_METHODS
                or request.user.is_admin
        )

        # return request.user.is_authenticated and (
        #     request.user.is_staff
        #     or request.user.is_superuser
        # )
