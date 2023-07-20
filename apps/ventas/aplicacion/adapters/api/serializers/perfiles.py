from rest_framework import serializers

from apps.ventas.aplicacion.adapters.api.serializers.cargos import CargoSerializer
from apps.ventas.aplicacion.adapters.api.serializers.usuarios import UsuarioSerializer
from apps.ventas.aplicacion.adapters.api.serializers.zonas import ZonaSerializer
from apps.ventas.aplicacion.use_cases.perfiles import PerfilUseCase
from apps.ventas.aplicacion.domain.models.perfiles import Perfil


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'cargo', 'zonas']
        read_only_fields = ['id']

    def create(self, validated_data):
        usuario = validated_data.pop('usuario')
        cargo = validated_data.pop('cargo')
        zonas = validated_data.pop('zonas')

        perfil_use_case = PerfilUseCase()
        perfil = perfil_use_case.create_perfil(usuario, cargo, zonas)
        return perfil

    def update(self, instance, validated_data):
        cargo = validated_data.pop('cargo')
        zonas = validated_data.pop('zonas')

        perfil_use_case = PerfilUseCase()
        perfil = perfil_use_case.update_perfil(instance, cargo, zonas)
        return perfil

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['usuario'] = UsuarioSerializer(instance.usuario).data
        representation['cargo'] = CargoSerializer(instance.cargo).data
        representation['zonas'] = ZonaSerializer(instance.zonas.all(), many=True).data

        return representation
