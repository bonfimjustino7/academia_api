from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class DadosBasicos(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        abstract = True


class UserCustom(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=255)
