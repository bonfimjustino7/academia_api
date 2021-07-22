import datetime

from .models import Mensalidade
from rest_framework.test import APITestCase
from dateutil.relativedelta import relativedelta


def _get_date_mensalidades_mock():
    mensalidades = []
    for i in range(1, 13):
        mensalidades.append(
            {'dt_vencimento': str(datetime.datetime.now().date() + relativedelta(months=i))}
        )
    return mensalidades


class MatriculaTest(APITestCase):
    base_url_aluno = '/api/aluno/'
    base_url_academia = '/api/academia/'

    def setUp(self) -> None:
        data_aluno = {
            "nome": "Aluno",
            "email": "aluno@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "12345",
            "academia": 1,
        }
        data_academia = {
            "nome": "Academia",
            "email": "academia@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12345"
        }
        self.client.post(self.base_url_academia, data_academia)
        self.client.post(self.base_url_aluno, data_aluno)

    def test_count_mensalidades(self):
        count_mensalidades = Mensalidade.objects.count()
        self.assertEqual(count_mensalidades, 12)

    def test_vencimento_mensalidades(self):
        mensalidades_dict = _get_date_mensalidades_mock()

        mensalidades_queryset = Mensalidade.objects.values('dt_vencimento')
        mensalidades = []
        for value in mensalidades_queryset:
            v = value['dt_vencimento']
            mensalidades.append({'dt_vencimento': str(v)})

        self.assertEqual(mensalidades_dict, mensalidades)
