from rest_framework.permissions import BasePermission, SAFE_METHODS


class SimpleBasePermission(BasePermission):
    """
    Class base permission to Interprotection.
    """
    role = 'superadmin'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        property_name = 'has_{role}_permissions'.format(role=self.role)
        return getattr(request.user, property_name)


class SimpleReadPermission(BasePermission):
    """
    Class base read permission to Interprotection.
    """
    role = 'superadmin'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            property_name = 'has_{role}_permissions'.format(role=self.role)
            return getattr(request.user, property_name)

        return False


class SuperAdminPermission(SimpleBasePermission):
    """
    Custom permissions to allow only superadmins.
    """
    role = 'superadmin'


class AdminPermission(SimpleBasePermission):
    """
    Custom permissions to allow only admins.
    """
    role = 'admin'
