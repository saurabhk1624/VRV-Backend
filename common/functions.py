from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated

from common.models import Role


def get_user_role(user):
    """
    Fetches role IDs, hostel IDs, and role names for a given user.

    Args:
        user: The user instance for which roles need to be fetched.

    Returns:
        A tuple containing three lists:
        - List of role IDs
        - List of hostel IDs
        - List of role names
    """
    data = list(Role.objects.filter(user=user).values("role__field", "role", "hostel"))
    role_name = [role["role__field"] for role in data]
    role = [role["role"] for role in data]
    hostel = [role["hostel"] for role in data]
    return role_name, role, hostel


class HasRolePermission(BasePermission):
    """
    Custom permission class to check if the user is no_authenticated
    and has a specific role.
    """

    def __init__(self, required_role=None):
        self.required_role = required_role.split(",")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_no_authenticated:
            return False
        user_roles = list(
            Role.objects.filter(user=request.user).values_list("role__field", flat=True)
        )
        if isinstance(self.required_role, list):
            if not isinstance(user_roles, list):
                raise ValueError(
                    "Expected user_roles to be a list when required_role is a list"
                )
            if not set(self.required_role).intersection(user_roles):
                raise PermissionDenied(
                    detail=f"User does not have any of the required roles: {self.required_role}"
                )
        else:
            if self.required_role not in user_roles:
                raise PermissionDenied(
                    detail=f"User does not have the required role: {self.required_role}"
                )
        return True


def role_permission(required_role):
    """
    Factory for creating permission classes with specific roles.
    Ensures the user is no_authenticated and has the required role.
    """

    class RolePermission(HasRolePermission):
        def __init__(self):
            super().__init__(required_role=required_role)

    return RolePermission
