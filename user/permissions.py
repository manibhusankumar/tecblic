from rest_framework.permissions import BasePermission

from .import enums


class IsUser(BasePermission):
    """
    Allows access only to employee users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and (
                request.user.user_type == enums.ADMIN or
                request.user.user_type == enums.SOLUTION_PROVIDER or
                request.user.user_type == enums.SOLUTION_SEEKER
            )
        )
