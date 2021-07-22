from django.db import models
from aluno.models import Aluno
from academia.models import Academia
from .constants import MESES, STATUS_MATRICULA, STATUS_MENSALIDADE, NAO_PAGO, ATIVA
from .managers import MensalidadeManager


class Matricula(models.Model):
    status = models.CharField(choices=STATUS_MATRICULA, max_length=2, default=ATIVA)
    dt_matricula = models.DateTimeField(auto_now_add=True)
    academia = models.ForeignKey(Academia, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['academia', 'aluno']

    def __str__(self):
        return f'#{self.id} -  {self.aluno.user.username} - {self.academia.user.username} - {self.get_status_display()}'


class Mensalidade(models.Model):
    dt_emissao = models.DateField(auto_now_add=True)
    mes_referente = models.IntegerField(choices=MESES)
    ano = models.IntegerField()
    dt_vencimento = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_MENSALIDADE, default=NAO_PAGO)
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)

    objects = MensalidadeManager()

    def __str__(self):
        return f'#{self.id} - {self.matricula.aluno} - {self.matricula.academia}'
