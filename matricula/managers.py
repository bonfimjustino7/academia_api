from django.db import models
import datetime
from dateutil.relativedelta import relativedelta


class MensalidadeManager(models.Manager):
    def generate_mensalidades(self, matricula):
        now = datetime.date.today()
        mensalidades = []
        for mes in range(1, 13):
            data_vencimento = now + relativedelta(months=mes)
            mensalidade = self.model(matricula=matricula, dt_vencimento=data_vencimento,
                                     mes_referente=now.month, ano=now.year)
            mensalidades.append(mensalidade)

        self.bulk_create(mensalidades)

    def pagar(self, matricula, mes, ano):
        from .constants import NAO_PAGO, PAGO
        ultima_mensalidade_valida = self.filter(matricula=matricula, mes_referente=mes, ano=ano,
                                                status=NAO_PAGO)
        if ultima_mensalidade_valida:
            mensalidade = ultima_mensalidade_valida.last()
            mensalidade.status = PAGO
            mensalidade.save()
            return True
        return False
