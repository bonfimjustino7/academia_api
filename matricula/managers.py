from django.db import models
import datetime
from dateutil.relativedelta import relativedelta


class MensalidadeManager(models.Manager):
    def generate_mensalidades(self, matriucula):
        from .models import Mensalidade
        now = datetime.date.today()
        mensalidades = []
        for mes in range(1, 13):
            data_vencimento = now + relativedelta(months=mes)
            mensalidade = Mensalidade(matricula=matriucula, dt_vencimento=data_vencimento,
                                      mes_referente=data_vencimento.month)
            mensalidades.append(mensalidade)

        Mensalidade.objects.bulk_create(mensalidades)
