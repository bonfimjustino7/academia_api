from django.db import models

from .managers import AlunoManagers
from auth_api.models import DadosBasicos


class Aluno(DadosBasicos):
    cpf = models.CharField(max_length=11, null=True, blank=True)

    objects = AlunoManagers()

    def __str__(self):
        return self.user.username