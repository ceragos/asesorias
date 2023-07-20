from django.contrib.auth.models import User

from apps.ventas.aplicacion.domain.models.perfiles import Perfil
from apps.ventas.aplicacion.ports.input_ports.perfiles import PerfilInputPort

class UsuarioUseCase(PerfilInputPort):

    def create_usuario(self, username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def delete_usuario(self, usuario_id):
        User.objects.filter(id=usuario_id).delete()
