from rest_framework.permissions import BasePermission

class CanAddDepartment(BasePermission):
    def has_permission(self, request, view):
        # Get the user's role (assuming your model structure)
        user_role = request.user.role

        # Check if the user role has the required permission
        has_permission = user_role.rolepermission_set.filter(
            permission__codename='add_department'
        ).exists()

        return has_permission
    

class CanDeleteDepartment(BasePermission):
    def has_permission(self, request, view):
        # Get the user's role (assuming your model structure)
        user_role = request.user.role

        # Check if the user role has the required permission
        has_permission = user_role.rolepermission_set.filter(
            permission__codename='delete_department'
        ).exists()

        return has_permission
    

class CanChangeDepartment(BasePermission):
    def has_permission(self, request, view):
        # Get the user's role (assuming your model structure)
        user_role = request.user.role

        # Check if the user role has the required permission
        has_permission = user_role.rolepermission_set.filter(
            permission__codename='change_department'
        ).exists()

        return has_permission
    

class CanViewDepartment(BasePermission):
    def has_permission(self, request, view):
        # Get the user's role (assuming your model structure)
        user_role = request.user.role

        # Check if the user role has the required permission
        has_permission = user_role.rolepermission_set.filter(
            permission__codename='view_department'
        ).exists()

        return has_permission