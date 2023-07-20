# Asesorias

## Comandos basicos

### Configurando el contenedor

Para construir la imagen de docker

    $ docker-compose build

Para verificar la sintaxis con flake8

    $ docker-compose run web flake8

Para aplicar las migraciones

    $ docker-compose run web python manage.py migrate

Para cargar datos

    $ docker-compose run web python manage.py loaddata db.json

Para crear un super usuario

    $ docker-compose run web python manage.py createsuperuser

Para ejecurtar las pruebas

    $ docker-compose run web python manage.py test

Para iniciar el contenedor

    $ docker-compose up -d

Para detener el contenedor

    $ docker-compose down
