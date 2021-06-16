from django.contrib.auth.hashers import make_password
from django.db import models
from rest_framework.authtoken.models import Token


class Academia(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, null=True, blank=True, unique=True)
    email = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    endereco = models.CharField(max_length=255)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.senha = make_password(self.senha)
        super(Academia, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nome


class TokenAcademia(Token):
    user = models.OneToOneField(
        Academia, related_name='academia_token',
        on_delete=models.CASCADE)
    key = models.CharField("Key", max_length=40, primary_key=True)
