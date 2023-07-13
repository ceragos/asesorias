from django.db import models


class MESES_CHOICES(models.TextChoices):
    ENERO = 'Enero'
    FEBRERO = 'Febrero'
    MARZO = 'Marzo'
    ABRIL = 'Abril'
    MAYO = 'Mayo'
    JUNIO = 'Junio'
    JULIO = 'Julio'
    AGOSTO = 'Agosto'
    SEPTIEMBRE = 'Septiembre'
    OCTUBRE = 'Octubre'
    NOVIEMBRE = 'Noviembre'
    DICIEMBRE = 'Diciembre'
