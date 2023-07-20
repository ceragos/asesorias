from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ventas.api.serializers import ClasificarSerializer, BalanceSerializer


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
