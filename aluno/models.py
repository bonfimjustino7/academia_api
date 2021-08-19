from django.db import models

from .managers import AlunoManagers
from auth_api.models import DadosBasicos


class Aluno(DadosBasicos):
    cpf = models.CharField(max_length=11, null=True, blank=True)

    objects = AlunoManagers()

    def __str__(self):
        return self.user.username


class Medicao(models.Model):
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    braco_direito = models.FloatField(null=True, blank=True)
    braco_esquerdo = models.FloatField(null=True, blank=True)
    antebraco_direito = models.FloatField(null=True, blank=True)
    antebraco_esquerdo = models.FloatField(null=True, blank=True)
    ombro = models.FloatField(null=True, blank=True)
    peitoral = models.FloatField(null=True, blank=True)
    abdome = models.FloatField(null=True, blank=True)
    cintura = models.FloatField(null=True, blank=True)
    gluteo = models.FloatField(null=True, blank=True)
    coxa_direita = models.FloatField(null=True, blank=True)
    coxa_esquerda = models.FloatField(null=True, blank=True)
    panturrilha_direta = models.FloatField(null=True, blank=True)
    panturrilha_esquerda = models.FloatField(null=True, blank=True)

    data_criacao = models.DateField(auto_now_add=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='medicoes')

    def __str__(self):
        return str(self.aluno)
