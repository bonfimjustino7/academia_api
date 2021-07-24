from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import *

from academia.models import Academia
from aluno.models import Aluno

User = get_user_model()


class AlunoTest(APITestCase):
    base_url_aluno = '/api/aluno/'
    base_url_academia = '/api/academia/'

    def create_academia(self):
        data_academia = {
            "nome": "Academia",
            "email": "academia@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12345"
        }
        self.client.post(self.base_url_academia, data_academia)

    def setUp(self) -> None:
        self.create_academia()

        data = {
            "nome": "Aluno",
            "email": "aluno@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "12345",
            'academia': 1
        }
        data2 = {
            "nome": "Aluno2",
            "email": "aluno2@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "1234",
            'academia': 1
        }

        self.client.post(self.base_url_aluno, data)
        self.client.post(self.base_url_aluno, data2)

    def test_create_aluno(self):
        """
        Testa criação de aluno
        """
        data = {
            "nome": "aluno 3",
            "email": "aluno3@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "123456",
            "academia": 1
        }
        response = self.client.post(self.base_url_aluno, data)
        if response.status_code != status.HTTP_201_CREATED:  # debug
            print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_aluno(self):
        pk = 2
        self.base_url_aluno += str(pk) + '/'
        data = {
            'id': pk,
            "nome": "aluno 4",
            "email": "aluno4@gmail.com",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "123456",
            "academia": 1,
        }
        user = Aluno.objects.get(pk=pk).user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.put(self.base_url_aluno, data)
        self.assertEqual(data, response.json())

    def test_create_and_update_aluno_cpf_and_email_duplicated(self):
        # create
        data = {
            "nome": "aluno",
            "email": "aluno@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "123425",
            "academia": 1
        }
        response = self.client.post(self.base_url_aluno, data)
        self.assertEqual(response.json(),
                         {'email': ['Este email já está sendo usado por outro usuário'],})

        # update
        pk = 2
        data_new = {
            "nome": "aluno Nova",
            "email": "alunonova@gmail.com",
            "password": "1234",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cpf": "12345",
            "academia": 1
        }
        self.base_url_aluno += str(pk) + '/'
        user = Aluno.objects.get(pk=pk).user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.put(self.base_url_aluno, data_new)
        self.assertEqual({'cpf': ['Este cpf já está sendo usado por outro usuário']}, response.json())

    def test_delete_aluno(self):
        pk = 1
        msg = ''
        self.base_url_aluno+= str(pk) + '/'
        user = Aluno.objects.get(pk=pk).user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.delete(self.base_url_aluno)
        if response.content:
            msg = response.json()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=msg)