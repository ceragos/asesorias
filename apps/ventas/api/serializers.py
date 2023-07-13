from rest_framework import serializers

from apps.ventas.models import MESES_CHOICES


class ClasificarSerializer(serializers.Serializer):
    sin_clasificar = serializers.ListField(child=serializers.IntegerField())


class BalanceSerializer(serializers.Serializer):
    mes = serializers.ListField(child=serializers.ChoiceField(choices=MESES_CHOICES.choices))
    ventas = serializers.ListField(child=serializers.IntegerField())
    gastos = serializers.ListField(child=serializers.IntegerField())


    def validate(self, data):
        mes = data.get('mes', [])
        ventas = data.get('ventas', [])
        gastos = data.get('gastos', [])

        if len(set(mes)) != len(mes):
            raise serializers.ValidationError({'mes': "El campo no debe contener elementos repetidos."})
        
        if len(mes) != len(ventas) or len(mes) != len(gastos) or len(ventas) != len(gastos):
            raise serializers.ValidationError("Las listas 'mes', 'ventas' y 'gastos' deben tener el mismo tamaño.")
        
        return data
