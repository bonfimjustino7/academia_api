from django.db import models
from auth_api.models import DadosBasicos


class Academia(DadosBasicos):
    cnpj = models.CharField(max_length=14, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username
