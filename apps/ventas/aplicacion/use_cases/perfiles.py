from apps.ventas.aplicacion.ports.input_ports.perfiles import PerfilInputPort
from apps.ventas.aplicacion.ports.output_ports.perfiles import PerfilOutputPort
from apps.ventas.aplicacion.domain.models.perfiles import Perfil


class PerfilUseCase(PerfilInputPort, PerfilOutputPort):

    def get_perfil(self, perfil_id):
        perfil = Perfil.objects.get(id=perfil_id)
        return perfil

    def list_perfiles(self):
        perfiles = Perfil.objects.all()
        return perfiles

    def create_perfil(self, usuario, cargo, zonas):
        perfil = Perfil.objects.create(usuario=usuario, cargo=cargo)
        perfil.zonas.set(zonas)
        perfil.save()
        return perfil

    def update_perfil(self, instance, cargo, zonas):
        perfil = instance
        perfil.cargo = cargo
        perfil.zonas.set(zonas)
        perfil.save()
        return perfil

    def delete_perfil(self, perfil_id):
        perfil = Perfil.objects.get(id=perfil_id)
        usuario_id = perfil.usuario.id
        perfil.delete()
        return usuario_id
