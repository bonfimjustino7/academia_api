from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import *

User = get_user_model()


class AcademiaTest(APITestCase):
    base_url = '/api/academia/'

    def setUp(self) -> None:
        data = {
            "nome": "Academia",
            "email": "academia@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12345"
        }
        data2 = {
            "nome": "Academia2",
            "email": "academia2@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "1234"
        }
        self.client.post(self.base_url, data)
        self.client.post(self.base_url, data2)

    def test_create_academia(self):
        """
        Testa criação de academia
        """
        data = {
            "nome": "Academia 3",
            "email": "academia3@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "123456"
        }
        response = self.client.post(self.base_url, data)
        if response.status_code != status.HTTP_201_CREATED:  # debug
            print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_academia(self):
        pk = 2
        self.base_url += str(pk) + '/'
        data = {
            'id': pk,
            "nome": "Academia 4",
            "email": "academia4@gmail.com",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "123456",
        }
        user = User.objects.get(pk=pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.put(self.base_url, data)
        self.assertEqual(data, response.json())

    def test_create_and_update_academia_cpf_and_email_duplicated(self):
        # create
        data = {
            "nome": "Academia",
            "email": "academia@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12347"
        }
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.json(),
                         {'email': ['Este email já está sendo usado por outro usuário']})

        # update
        pk = 2
        data_new = {
            "nome": "Academia Nova",
            "email": "academianova@gmail.com",
            "password": "1234",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "12345"
        }
        self.base_url += str(pk) + '/'
        user = User.objects.get(pk=pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.put(self.base_url, data_new)
        self.assertEqual({'cnpj': ['Este cnpj já está sendo usado por outro usuário']}, response.json())

    def test_delete_academia(self):
        pk = 1
        msg = ''
        self.base_url += str(pk) + '/'
        user = User.objects.get(pk=pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.delete(self.base_url)
        if response.content:
            msg = response.json()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=msg)