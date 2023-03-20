from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_authenticated or
                request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or
                request.method in SAFE_METHODS or
                request.user.is_admin
                )


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_admin
