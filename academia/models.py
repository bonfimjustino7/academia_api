from django.contrib.auth import get_user_model
from django.db import models

from academia.managers import AcademiaManager
from auth_api.models import DadosBasicos

User = get_user_model()


class Academia(DadosBasicos):
    cnpj = models.CharField(max_length=14, null=True, blank=True, unique=True)

    objects = AcademiaManager()

    def __str__(self):
        return self.user.username
