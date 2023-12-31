from django.db import transaction
from typing import List

from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.ventas.aplicacion.adapters.api.serializers.perfiles import PerfilSerializer
from apps.ventas.aplicacion.adapters.api.serializers.usuarios import UsuarioSerializer
from apps.ventas.aplicacion.use_cases.perfiles import PerfilUseCase
from apps.ventas.aplicacion.use_cases.usuarios import UsuarioUseCase


class PerfilAdapter(APIView):
    permission_classes: List[BasePermission] = [IsAuthenticated]
    perfil_use_case: PerfilUseCase = None

    def get(self, request: Request) -> Response:
        perfiles = self.perfil_use_case.list_perfiles()
        perfiles_serializer = PerfilSerializer(perfiles, many=True)
        return Response(perfiles_serializer.data)

    def post(self, request: Request) -> Response:
        with transaction.atomic():
            try:
                usuario_serializer = UsuarioSerializer(data=request.data)
                usuario_serializer.is_valid(raise_exception=True)
                usuario = usuario_serializer.save()

                perfil_data = request.data.copy()
                perfil_data['usuario'] = usuario.id
                perfil_serializer = PerfilSerializer(data=perfil_data)
                perfil_serializer.is_valid(raise_exception=True)
                perfil_serializer.save()
                data = perfil_serializer.data
            except Exception as e:
                transaction.set_rollback(True)
                raise e
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request, perfil_id: int) -> Response:
        perfil = self.perfil_use_case.get_perfil(perfil_id)
        perfil_serializer = PerfilSerializer(instance=perfil, data=request.data, partial=True)
        perfil_serializer.is_valid(raise_exception=True)
        perfil_serializer.save()
        return Response(perfil_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, perfil_id: int) -> Response:
        usuario_id = self.perfil_use_case.delete_perfil(perfil_id)
        usuario_use_case = UsuarioUseCase()
        usuario_use_case.delete_usuario(usuario_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
