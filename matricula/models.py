import datetime

from django.db import models
from aluno.models import Aluno
from academia.models import Academia
from .constants import MESES, STATUS_MATRICULA, STATUS_MENSALIDADE, NAO_PAGO, ATIVA, NULA, PAGO, \
    MEIOS_PAGAMENTO, RAZOES
from .managers import MensalidadeManager
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


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
    razao_nulo = models.CharField(max_length=50, choices=RAZOES, null=True, blank=True)
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    valor = models.FloatField(default=0.0)
    meio_pagamento = models.CharField(max_length=3, choices=MEIOS_PAGAMENTO)
    objects = MensalidadeManager()

    def anular(self, motivo, criar_nova=False):
        if self.status == NULA:
            raise ValidationError(f'Esta mensalidade já foi anulada')

        razoes_validas = list(map(lambda meios: meios[0], RAZOES))
        if motivo in razoes_validas:
            self.status = NULA
            self.razao_nulo = motivo
            if criar_nova:
                Mensalidade.objects.generate_mensalidades(self.matricula.id, self.valor, self.mes_referente,
                                                   self.ano)
        else:
            raise ValidationError(f'Razão inválida, solicite as disponiveis: {razoes_validas}')

    def pagar(self, meio_pagamento, criar_nova=False):
        if self.status == NAO_PAGO:
            self.status = PAGO
            self.meio_pagamento = meio_pagamento
            if criar_nova:
                dia_vencimento = self.dt_vencimento.day
                proximo_data_pagamento = datetime.date(year=self.ano, month=self.mes_referente, day=dia_vencimento) + relativedelta(months=1)
                Mensalidade.objects.generate_mensalidades(self.matricula.id, self.valor,
                                                          proximo_data_pagamento.month,
                                                          self.ano)
        elif self.status == PAGO:
            raise ValidationError(f'Mensalidade já está {self.get_status_display()}')
        else:
            raise ValidationError(f'Mensalidade com o status {self.get_status_display()} não pode ser paga.')

    def __str__(self):
        return f'#{self.id} - {self.matricula.aluno} - {self.matricula.academia}'
