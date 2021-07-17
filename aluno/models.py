from django.db import models
from auth_api.models import DadosBasicos


class Aluno(DadosBasicos):
    cpf = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.user.username