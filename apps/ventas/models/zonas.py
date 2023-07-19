from django.db import models

from apps.ventas.behaviors.parametros import Parametro


class Zona(Parametro):
    ciudad = models.CharField(max_length=80)

    def __str__(self) -> str:
        return f'{self.ciudad} - {self.nombre}'
