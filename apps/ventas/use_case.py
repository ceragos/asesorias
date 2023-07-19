from django.contrib.auth.models import User
from apps.ventas.models.perfiles import Perfil


class PerfilUseCase:

    def delete_perfil(self, perfil_id):
        perfil = Perfil.objects.get(id=perfil_id)
        usuario_id = perfil.usuario.id
        perfil.delete()
        User.objects.filter(id=usuario_id).delete()
