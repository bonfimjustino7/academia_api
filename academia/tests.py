from rest_framework import status
from rest_framework.test import *


class AcademiaTest(APITestCase):
    base_url = '/api/academia/'

    def test_create_academia(self):
        """
        Testa criação de academia
        """
        data = {
            "nome": "Academia 1",
            "email": "academia1@gmail.com",
            "password": "123",
            "telefone": "8899211128",
            "endereco": "Rua funlando de tal",
            "cnpj": "1234"
        }
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_update_academia(self):
    #     pk = '1/'
    #     self.base_url += pk
    #     data = {
    #         "nome": "Academia2",
    #         "email": "academia@gmail.com",
    #         "telefone": "8899211128",
    #         "endereco": "Rua funlando de tal",
    #         "cnpj": "1234"
    #     }
    #     response = self.client.put(self.base_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
