from rest_framework import permissions

from tenant.models import Role


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Superadmin can update/delete any user.
    Admin users can update/delete any user  except superuser.
    Users can update/delete only their own data.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        # If the user is an admin, they can update any profile
        if user.is_superuser:
            return True
        if user.is_admin and user.organization == obj.organization:
            if obj.role.name != Role.SUPERUSER:
                return True
            return False
        # If the user is updating their own profile, allow the action
        if user.organization == obj.organization:
            if request.method in permissions.SAFE_METHODS:
                return True
            if user == obj:
                return True
            return False
        return False


class ObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        elif user.is_admin and user.organization_id == obj.organization_id:
            return True
        else:
            if request.method in permissions.SAFE_METHODS and user.organization_id == obj.organization_id:
                return True
            return False


class OrganizationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        elif user.is_admin and user.organization_id == obj.id:
            return True
        else:
            if request.method in permissions.SAFE_METHODS and user.organization_id == obj.id:
                return True
            return False
