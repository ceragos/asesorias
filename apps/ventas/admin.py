from django.contrib import admin

from apps.ventas.aplicacion.domain.models.cargos import Cargo
from apps.ventas.aplicacion.domain.models.zonas import Zona
from apps.ventas.aplicacion.domain.models.perfiles import Perfil


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nombre']


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['ciudad', 'nombre']


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario']
