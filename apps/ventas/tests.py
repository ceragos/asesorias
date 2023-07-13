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

    