from rest_framework import serializers

from apps.ventas.aplicacion.domain.models.perfiles import Cargo


class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = ['nombre']
