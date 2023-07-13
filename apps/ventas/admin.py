from django.contrib import admin

from apps.ventas.models import Cargo, Zona, Perfil


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nombre']


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['ciudad', 'nombre']


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario']
