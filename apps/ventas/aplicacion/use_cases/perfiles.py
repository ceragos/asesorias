from typing import List
from django.contrib.auth.models import User

from apps.ventas.aplicacion.ports.input_ports.perfiles import PerfilInputPort
from apps.ventas.aplicacion.ports.output_ports.perfiles import PerfilOutputPort
from apps.ventas.aplicacion.domain.models.perfiles import Perfil
from apps.ventas.aplicacion.domain.models.cargos import Cargo
from apps.ventas.aplicacion.domain.models.zonas import Zona


class PerfilUseCase(PerfilInputPort, PerfilOutputPort):

    def get_perfil(self, perfil_id: Perfil) -> Perfil:
        perfil = Perfil.objects.get(id=perfil_id)
        return perfil

    def list_perfiles(self) -> List[Perfil]:
        perfiles = Perfil.objects.all()
        return perfiles

    def create_perfil(self, usuario: User, cargo: Cargo, zonas: List[Zona]) -> Perfil:
        perfil = Perfil.objects.create(usuario=usuario, cargo=cargo)
        perfil.zonas.set(zonas)
        perfil.save()
        return perfil

    def update_perfil(self, perfil: Perfil, cargo: Cargo, zonas: List[Zona]) -> Zona:
        perfil.cargo = cargo
        perfil.zonas.set(zonas)
        perfil.save()
        return perfil

    def delete_perfil(self, perfil_id: int) -> int:
        perfil = Perfil.objects.get(id=perfil_id)
        usuario_id = perfil.usuario.id
        perfil.delete()
        return usuario_id
