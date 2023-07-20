## Requisitos

Asegúrate de tener instalado lo siguiente en tu entorno de desarrollo:

- Python (versión 3)

## Configuración del Entorno

1. Clona este repositorio en tu máquina local:

```
git clone https://github.com/ceragos/asesorias
```

2. Accede al directorio del proyecto:

```
cd asesorias
```

3. Crea un entorno virtual para el proyecto:

```
python -m venv env
```

4. Activa el entorno virtual:

- En Windows:

```
env\Scripts\activate
```

- En macOS y Linux:

```
source env/bin/activate
```

5. Instala las dependencias del proyecto:

```
pip install -r requirements.txt
```

6. Realiza las migraciones de la base de datos:

```
python manage.py migrate
```

## Cargar datos

```
python manage.py loaddata db.json
```

## Ejecución del Proyecto

1. Inicia el servidor de desarrollo:

```
python manage.py runserver
```

2. Abre tu navegador web y accede a la siguiente URL:

```
http://localhost:8000
```

## Ejecucion de pruebas

```
python manage.py test
```
