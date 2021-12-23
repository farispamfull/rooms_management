from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthenticatedOrStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_staff
            or request.method in SAFE_METHODS
        )
