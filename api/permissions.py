from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthenticatedOrStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_staff
                 or request.method in SAFE_METHODS)
        )


class AuthenticatedOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and obj.user == request.user
            or request.user.is_staff
        )


class AuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action == 'list':
                return request.user.is_staff
            return True
        return False
