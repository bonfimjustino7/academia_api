from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class DadosBasicos(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        abstract = True


class Academia(DadosBasicos):
    cnpj = models.CharField(max_length=14, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username
