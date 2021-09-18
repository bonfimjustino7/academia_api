from django.db import models
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings

from matricula.constants import NAO_PAGO, ERRO_CONTABIL


class MensalidadeManager(models.Manager):

    def anular_mensalidade_mes_duplicados(self, matricula_id, mes_referente, ano):
        mensalidadade = self.filter(matricula_id=matricula_id, mes_referente=mes_referente, ano=ano,
                                    status=NAO_PAGO).last()
        if mensalidadade:
            mensalidadade.anular(ERRO_CONTABIL)
            mensalidadade.save()

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        # caso seja sqlite não utilizar o bulk_create, pois não retorna o obj com id
        if 'sqlite3' not in settings.DATABASES[self.db]['ENGINE']:
            return super(MensalidadeManager, self).bulk_create(objs, batch_size, ignore_conflicts)

        for obj in objs:
            obj.save()
        return objs

    def generate_mensalidades(self, matricula, valor, mes_referente, ano, qtd_parcelas=1):
        """
        Gera mensalidades de uma matricula

        @param matricula id da matricula do aluno
        @param valor valor da matricula
        @param mes_referente mes referente em int. Ex.: 1 - Janeiro, 2- Fevereiro
        @param ano ano da mensalidade
        @param qtd_parcelas número de parcelas a serem geradas
        @return Quantidade de mensalidades criadas
        """
        self.anular_mensalidade_mes_duplicados(matricula, mes_referente, ano)
        now = datetime.date.today()
        data_referente = datetime.date(year=ano, month=mes_referente, day=now.day)
        mensalidades = []
        for mes in range(1, qtd_parcelas + 1):
            data_vencimento = data_referente + relativedelta(months=mes)
            mensalidade = self.model(matricula_id=matricula, dt_vencimento=data_vencimento,
                                     mes_referente=mes_referente, ano=data_vencimento.year,
                                     valor=valor)
            mensalidades.append(mensalidade)

        return self.bulk_create(mensalidades)
