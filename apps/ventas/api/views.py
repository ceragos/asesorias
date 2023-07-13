from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db import transaction

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


class UsuarioViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            try:
                user = serializer.save()
                perfil_data = {'usuario': user.id, 'cargo': request.data.get('cargo'), 'zonas': request.data.get('zonas')}
                perfil_serializer = PerfilSerializer(data=perfil_data)
                perfil_serializer.is_valid(raise_exception=True)
                perfil_serializer.save()
            except Exception as e:
                transaction.set_rollback(True)
                raise e
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)