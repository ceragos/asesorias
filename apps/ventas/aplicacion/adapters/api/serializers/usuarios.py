from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from apps.ventas.aplicacion.use_cases.usuarios import UsuarioUseCase


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
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')

        usuario_use_case = UsuarioUseCase()
        user = usuario_use_case.create_usuario(username, password)
        return user
