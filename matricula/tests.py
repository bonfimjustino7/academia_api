import datetime

from aluno.models import Aluno
from .models import Mensalidade
from rest_framework.test import APITestCase
from dateutil.relativedelta import relativedelta


def _get_date_mensalidades_mock():
    mensalidades = []
    for i in range(0, 12):
        mensalidades.append(
            {'dt_vencimento': str(datetime.datetime.now().date() + relativedelta(months=i))}
        )
    return mensalidades


class MatriculaTest(APITestCase):
    base_url_aluno = '/api/aluno/'
    base_url_academia = '/api/academia/'
    base_url_mensalidade = '/api/matricula/1/mensalidades/'

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

    def test_list_mensalidades(self):
        user = Aluno.objects.get(pk=1).user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.get(self.base_url_mensalidade)

        self.assertEqual(response.status_code, 200)

    def test_criar_mensalidade(self):
        mensalidades = Mensalidade.objects.generate_mensalidades(1, 50.0, 9, 2021)
        self.assertEqual(len(mensalidades), 1)