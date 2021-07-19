from .models import Matricula, Mensalidade
from academia.models import Academia
from aluno.models import Aluno
from rest_framework.test import APITestCase


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
            "cpf": "12345"
        }
        data_academia = {
            "nome": "Academia",
            "email": "academia@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12345"
        }
        self.client.post(self.base_url_aluno, data_aluno)
        self.client.post(self.base_url_academia, data_academia)
        academia = Academia.objects.all().first()
        aluno = Aluno.objects.all().first()
        Matricula.objects.create(aluno=aluno, academia=academia)

    def test_count_mensalidades(self):
        count_mensalidades = Mensalidade.objects.count()
        self.assertEqual(count_mensalidades, 12)

    def test_vencimento_mensalidades(self):
        mensalidades_dict = [
               {'dt_vencimento': '2021-08-18'},
               {'dt_vencimento': '2021-09-18'},
               {'dt_vencimento': '2021-10-18'},
               {'dt_vencimento': '2021-11-18'},
               {'dt_vencimento': '2021-12-18'},
               {'dt_vencimento': '2022-01-18'},
               {'dt_vencimento': '2022-02-18'},
               {'dt_vencimento': '2022-03-18'},
               {'dt_vencimento': '2022-04-18'},
               {'dt_vencimento': '2022-05-18'},
               {'dt_vencimento': '2022-06-18'},
               {'dt_vencimento': '2022-07-18'},
        ]

        mensalidades_queryset = Mensalidade.objects.values('dt_vencimento')
        mensalidades = []
        for value in mensalidades_queryset:
            v = value['dt_vencimento']
            mensalidades.append({'dt_vencimento': str(v)})

        self.assertEqual(mensalidades_dict, mensalidades)
