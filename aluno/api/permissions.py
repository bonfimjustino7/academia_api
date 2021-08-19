from rest_framework.permissions import BasePermission

from matricula.constants import ATIVA
from matricula.models import Matricula


class IsAlunoPermission(BasePermission):
    """
    Permite o acesso somente ao aluno ou academia do aluno
    """

    def has_permission(self, request, view):
        """
         Se for autenticado
        """
        return bool(
            request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
            Se for o usuário que criou ou a academia que o aluno está matriculado
        """
        return bool(
            obj.user and request.auth.user == obj.user or
            Matricula.objects.filter(academia__user=request.auth.user, status=ATIVA).count() == 1
        )

