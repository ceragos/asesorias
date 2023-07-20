from rest_framework import serializers

from apps.ventas.aplicacion.domain.models.perfiles import Zona


class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        fields = ['ciudad', 'nombre']
