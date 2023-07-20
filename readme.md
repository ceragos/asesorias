# Asesorias
![Prueba de desarrollador backend](badges/backend.svg)

Este proyecto consta de tres endpoints de una API diseñada para procesar datos y realizar operaciones relacionadas con una matriz de números, un diccionario de información de ventas y gastos, un esquema de base de datos con usuarios y un sistema de autenticación básica (Basic Auth) para el acceso a los endpoints.

### Tecnologías Utilizadas
El proyecto ha sido desarrollado utilizando las siguientes tecnologías:

- Lenguaje de Programación: Python
- Framework/API: Django Rest Framework
- Base de Datos: PosgreSQL
- Autenticación: Basic Auth
- Contenerización: Docker
### 1) Ordenar una Matriz de Números

Este endpoint recibe una matriz de números y devuelve la misma matriz ordenada, con la particularidad de que los números duplicados se mueven al final de la lista ordenada.

    POST /api/clasificar/

    {
        "sin_clasificar": [3,5,5,6,8,3,4,4,7,7,1,1,2]
    }

### 2) Información de Ventas y Gastos con Balance
Este endpoint recibe un diccionario con información sobre ventas y gastos de diferentes meses y devuelve un JSON con la información recibida, incluyendo el balance de cada mes (Ventas - Gastos).

    POST /api/balance/

    {
        "mes":["Enero", "Febrero", "Marzo", "Abril"],
        "ventas":[30500, 35600, 28300, 33900],
        "gastos":[22000, 23400, 18100, 20700]
    }

### 3) Esquema de Base de Datos para Usuarios
En este endpoint se ha creado un esquema de base de datos con los modelos, perfil, cargo y zona. tambien se hace uso del modelo de usuario(user) de django, y se ha implementado un servicio que permite añadir, consultar, modificar y eliminar la información de los perfiles, que tendra relacion con todos los modelos mencionados.

Para obtener el listado de perfiles

    GET api/perfiles/

Para crear un nuevo perfil

    POST /api/perfiles/

    {
        "username": "maestro",
        "password": "unaClave12345678",
        "password_confirmation": "unaClave12345678",
        "cargo": 1,
        "zonas": [1, 2]
    }

Para modificar los datos del perfil

    PATCH /api/perfiles/1/

    {
        "cargo": 1,
        "zonas": [2]
    }

Para eliminar un perfil

    DELETE /api/perfiles/1/

Para ejecutar el programa lee las [instrucciones](docs/docker.md)
