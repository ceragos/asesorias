from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ventas.api.serializers import ClasificarSerializer

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

