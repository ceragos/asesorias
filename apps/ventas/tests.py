import base64

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status, HTTP_HEADER_ENCODING


class VentasTestCase(APITestCase):

    def setUp(self):
        username = 'maestro'
        password = 'hX$9bC1J6Q7X'

        User.objects.create_user(username=username, password=password)

        credentials = f"{username}:{password}".encode(HTTP_HEADER_ENCODING) 
        self.headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + 
            base64.b64encode(credentials).decode(HTTP_HEADER_ENCODING)
        }

    def test_clasificar(self):
        url = '/api/clasificar/'
        data = {
            'sin_clasificar': [3, 5, 5, 6, 8, 3, 4, 4, 7, 7, 1, 1, 2]
        }
        response = self.client.post(url, data, format='json', **self.headers)

        respuesta_esperada = {
            'sin_clasificar': [3, 5, 5, 6, 8, 3, 4, 4, 7, 7, 1, 1, 2],
            'clasificado': [1, 2, 3, 4, 5, 6, 7, 8, 5, 3, 4, 7, 1]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, respuesta_esperada)

    def test_balance(self):
        url = '/api/balance/'
        data = {
            "mes": ["Enero", "Febrero", "Marzo", "Abril"],
            "ventas": [30500, 35600, 28300, 33900],
            "gastos": [22000, 23400, 18100, 20700]
        }
        response = self.client.post(url, data, format='json', **self.headers)

        expected_data = [
            {
                "mes": "Enero",
                "ventas": 30500,
                "gastos": 22000,
                "balance": 8500
            },
            {
                "mes": "Febrero",
                "ventas": 35600,
                "gastos": 23400,
                "balance": 12200
            },
            {
                "mes": "Marzo",
                "ventas": 28300,
                "gastos": 18100,
                "balance": 10200
            },
            {
                "mes": "Abril",
                "ventas": 33900,
                "gastos": 20700,
                "balance": 13200
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

