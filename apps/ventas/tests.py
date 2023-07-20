import base64

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status, HTTP_HEADER_ENCODING

from apps.ventas.aplicacion.adapters.api.serializers.perfiles import PerfilSerializer
from apps.ventas.aplicacion.domain.models.cargos import Cargo
from apps.ventas.aplicacion.domain.models.zonas import Zona
from apps.ventas.aplicacion.domain.models.perfiles import Perfil


class VentasTestCase(APITestCase):

    def setUp(self):
        username = 'maestro'
        password = 'hX$9bC1J6Q7X'

        User.objects.create_user(username=username, password=password)
        credentials = f'{username}:{password}'.encode(HTTP_HEADER_ENCODING)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Basic '
            + base64.b64encode(credentials).decode(HTTP_HEADER_ENCODING)
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
            'mes': ['Enero', 'Febrero', 'Marzo', 'Abril'],
            'ventas': [30500, 35600, 28300, 33900],
            'gastos': [22000, 23400, 18100, 20700]
        }
        response = self.client.post(url, data, format='json', **self.headers)

        expected_data = [
            {
                'mes': 'Enero',
                'ventas': 30500,
                'gastos': 22000,
                'balance': 8500
            },
            {
                'mes': 'Febrero',
                'ventas': 35600,
                'gastos': 23400,
                'balance': 12200
            },
            {
                'mes': 'Marzo',
                'ventas': 28300,
                'gastos': 18100,
                'balance': 10200
            },
            {
                'mes': 'Abril',
                'ventas': 33900,
                'gastos': 20700,
                'balance': 13200
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class PerfilViewSetTestCase(APITestCase):

    def setUp(self):
        self.username = 'usuario_test1'
        self.password = 'hX$9bC1J6Q7X'
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.cargo = Cargo.objects.create(nombre='Asesor')
        self.zona1 = Zona.objects.create(ciudad='Cali', nombre='Sur')
        self.zona2 = Zona.objects.create(ciudad='Cali', nombre='Norte')

    def test_listar_perfiles(self):
        perfil1 = Perfil.objects.create(usuario=self.user, cargo=self.cargo)
        perfil1.zonas.add(self.zona1)

        usuario = User.objects.create_user(
            username='usuario_test2', password='hX$9bC1J6Q7X'
        )
        perfil2 = Perfil.objects.create(usuario=usuario, cargo=self.cargo)
        perfil2.zonas.add(self.zona2)

        url = '/api/perfiles/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        perfiles = Perfil.objects.all()
        serializer = PerfilSerializer(perfiles, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_registrar_perfil(self):
        url = '/api/perfiles/'
        data = {
            'username': 'usuario_test3',
            'password': 'hX$9bC1J6Q7X',
            'password_confirmation': 'hX$9bC1J6Q7X',
            'cargo': self.cargo.id,
            'zonas': [self.zona1.id, self.zona2.id]
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)

        perfil = Perfil.objects.get()
        self.assertEqual(perfil.usuario.username, 'usuario_test3')
        self.assertEqual(perfil.cargo, self.cargo)
        self.assertEqual(list(perfil.zonas.all()), [self.zona1, self.zona2])

    def test_modificar_perfil(self):
        perfil = Perfil.objects.create(usuario=self.user, cargo=self.cargo)
        perfil.zonas.add(self.zona1)

        url = f'/api/perfiles/{perfil.id}/'
        data = {
            'cargo': self.cargo.id,
            'zonas': [self.zona2.id]
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        perfil = Perfil.objects.get(id=perfil.id)
        serializer = PerfilSerializer(perfil)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(perfil.cargo, self.cargo)
        self.assertEqual(list(perfil.zonas.all()), [self.zona2])

    def test_eliminar_perfil(self):
        perfil = Perfil.objects.create(usuario=self.user, cargo=self.cargo)
        perfil.zonas.add(self.zona1)

        url = f'/api/perfiles/{perfil.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Perfil.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        self.assertTrue(Cargo.objects.filter(id=self.cargo.id).exists())
        self.assertTrue(Zona.objects.filter(id=self.zona1.id).exists())
