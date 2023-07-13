from rest_framework import serializers


class ClasificarSerializer(serializers.Serializer):
    sin_clasificar = serializers.ListField(child=serializers.IntegerField())
