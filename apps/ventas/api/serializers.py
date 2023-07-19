from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from apps.ventas.enums.meses import MESES_CHOICES
from apps.ventas.models.perfiles import Perfil, Cargo, Zona


class ClasificarSerializer(serializers.Serializer):
    sin_clasificar = serializers.ListField(child=serializers.IntegerField())


class BalanceSerializer(serializers.Serializer):
    mes = serializers.ListField(
        child=serializers.ChoiceField(choices=MESES_CHOICES.choices)
    )
    ventas = serializers.ListField(child=serializers.IntegerField())
    gastos = serializers.ListField(child=serializers.IntegerField())

    def validate(self, data):
        mes = data.get('mes', [])
        ventas = data.get('ventas', [])
        gastos = data.get('gastos', [])

        if len(set(mes)) != len(mes):
            raise serializers.ValidationError(
                {
                    'mes': 'El campo no debe contener elementos repetidos.'
                }
            )

        if (
            len(mes) != len(ventas)
            or len(mes) != len(gastos)
            or len(ventas) != len(gastos)
        ):
            raise serializers.ValidationError(
                "Las listas 'mes', 'ventas' y 'gastos' deben tener el mismo tamaño."
            )

        return data


class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = ['nombre']


class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        fields = ['ciudad', 'nombre']


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmation')

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError(
                {
                    'password': 'Las contraseñas no coinciden.'
                }
            )

        validate_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['usuario'] = UsuarioSerializer(instance.usuario).data
        representation['cargo'] = CargoSerializer(instance.cargo).data
        representation['zonas'] = ZonaSerializer(instance.zonas.all(), many=True).data

        return representation
