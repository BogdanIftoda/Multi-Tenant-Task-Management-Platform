from rest_framework import permissions
from rest_framework.permissions import BasePermission


# TODO: fix the permissions
class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only superusers and admins to create, update, or delete labels.
    Regular users can only read labels.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_admin:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if user.is_admin and obj.organization == user.organization:
            return True
        # Allow read-only access for all authenticated users
        if request.method in permissions.SAFE_METHODS and user.organization == obj.organization:
            return True

        return False
