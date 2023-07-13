from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db import transaction

from apps.ventas.models import Perfil
from apps.ventas.api.serializers import ClasificarSerializer, BalanceSerializer, UsuarioSerializer, PerfilSerializer

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def clasificar(request):
    serializer = ClasificarSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    sin_clasificar = serializer.validated_data['sin_clasificar']

    principal = []
    duplicado = []
    for elemento in sin_clasificar:
        if elemento not in principal:
            principal.append(elemento)
        else:
            duplicado.append(elemento)

    clasificado = sorted(principal) + duplicado
    
    response_data = {
        'sin_clasificar': sin_clasificar,
        'clasificado': clasificado
    }
    
    return Response(response_data)


class Balance(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resultado = []
        for mes, ventas, gastos in zip(data['mes'], data['ventas'], data['gastos']):
            item = {
                'mes': mes,
                'ventas': ventas,
                'gastos': gastos,
                'balance': ventas - gastos
            }
            resultado.append(item)
        return Response(resultado)


class PerfilViewSet(ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        usuario_serializer = UsuarioSerializer(data=request.data)
        usuario_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            try:
                perfil_data = request.data.copy()
                usuario = usuario_serializer.save()
                perfil_data['usuario'] = usuario.id
                perfil_serializer = self.get_serializer(data=perfil_data)
                perfil_serializer.is_valid(raise_exception=True)
                perfil_serializer.save()
            except Exception as e:
                transaction.set_rollback(True)
                raise e
        headers = self.get_success_headers(perfil_serializer.data)
        return Response(perfil_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        usuario_id = instance.usuario.id
        self.perform_destroy(instance)
        User.objects.filter(id=usuario_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
