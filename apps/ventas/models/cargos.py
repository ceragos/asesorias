from django.db import models

from apps.ventas.behaviors.parametros import Parametro


class Cargo(Parametro):
    actividades = models.TextField()
