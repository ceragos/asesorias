from django.db import models


class Parametro(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre
