from rest_framework.permissions import BasePermission


class IsAuthenticatedOwner(BasePermission):
    """
    Permite o acesso somente a usuários autenticados e que seja dono da conta
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user and request.auth.user == obj.user
        )

