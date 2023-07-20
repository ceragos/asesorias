class PerfilInputPort:

    def get_perfil(self):
        raise NotImplementedError()

    def create_perfil(self):
        raise NotImplementedError()

    def delete_perfil(self, perfil_id):
        raise NotImplementedError()
