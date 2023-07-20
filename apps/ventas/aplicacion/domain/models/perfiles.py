from django.db import models
from django.contrib.auth.models import User

from apps.ventas.aplicacion.domain.models.cargos import Cargo
from apps.ventas.aplicacion.domain.models.zonas import Zona


class Perfil(models.Model):
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, related_name='perfiles', on_delete=models.PROTECT)
    zonas = models.ManyToManyField(Zona, related_name='perfiles')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
