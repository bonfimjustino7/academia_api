from django.contrib.auth import get_user_model
from django.db import models

from auth_api.managers import UserManager
from auth_api.models import DadosBasicos
from matricula.constants import ATIVA, INATIVA

User = get_user_model()


class Academia(DadosBasicos):
    cnpj = models.CharField(max_length=14, null=True, blank=True, unique=True)

    objects = UserManager()

    @property
    def alunos_ativos(self):
        return self.matricula_set.filter(status=ATIVA).count()

    @property
    def alunos_inativos(self):
        return self.matricula_set.filter(status=INATIVA).count()

    def __str__(self):
        return self.user.username
