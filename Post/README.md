# Microservicio de Publicaciones

Este es un microservicio que se encarga de administrar publicaciones. Permite crear, consultar y eliminar publicaciones, así como filtrarlas por diferentes criterios. A continuación, se describen los detalles para ejecutar este microservicio.

## Tabla de contenido

- [Instalación](#Instalación)
- [Requisitos Previos](#Requisitos-previos)
- [Ejecución del Microservicio](#Ejecución-del-Microservicio)
- [Ejecución desde Dockerfile](#Ejecución-desde-Dockerfile)
- [Endpoints de la API](#Endpoints-de-la-API)
- [Pruebas Microservicio Publicaciones](#Pruebas-Microservicio-Publicaciones)

## Instalación

    Clona este repositorio: git clone https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo6
    Accede a la carpeta del proyecto: cd Post
    Crea un entorno virtual: python -m venv venv
    Activa el entorno virtual: source venv/bin/activate
    Instala las dependencias: pip install -r requirements.txt

### Dependencias que se instalaran

- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- gunicorn
- psycopg2-binary
- Faker
- coverage
- pytest
- pytest-cov
- pytest-mock
- pytest-env

## Requisitos Previos

Es importante asegurarse tener instalados los siguientes requisitos antes de ejecutar este microservicio:
Python: Se utiliza Python 3.9 en este microservicio.
Dependencias: Todas las dependencias necesarias están especificadas en el archivo requirements.txt. Puedes instalarlas utilizando **pip install -r requirements.txt**
Variables de Entorno: Se utilizan variables de entorno para configurar el servicio.
USERS_PATH: La URL para acceder a los endpoints de usuarios.

## Ejecución del Microservicio

Para ejecutar el microservicio, sigue estos pasos:

1. Asegúrate de que las variables de entorno estén configuradas correctamente.
2. Ejecuta el microservicio con el siguiente comando: python app.py
   El microservicio se ejecutará en http://localhost:3001 de forma predeterminada. Además se puede cambiar el puerto en el archivo de código si es necesario.
3. Puedes acceder a la API del microservicio a través de http://localhost:3001/posts.

## Ejecución desde Dockerfile

Este microservicio también se puede ejecutar en un contenedor Docker. Para hacerlo, sigue estos pasos:

1. Tener Docker instalado en tu sistema.
2. Construir la imagen del contenedor utilizando el siguiente comando (asegúrate de estar en la misma carpeta que el archivo Dockerfile): docker build publicaciones-app
3. Una vez que se haya construido la imagen, puedes ejecutar un contenedor a partir de ella:
4. Esto ejecutará el microservicio en un contenedor y mapeará el puerto 3001 del contenedor al puerto 3001 de tu máquina local. Docker run -p 3001:3001 publicaciones-app
5. El microservicio estará disponible en http://localhost:3001 de tu máquina local.

## Endpoints de la API

El microservicio ofrece los siguientes endpoints de la API:

**GET /posts:** Filtra y muestra publicaciones según varios criterios, como la expiración y la ruta.

**GET /posts/{id_publicacion}:** Consulta detalles de una publicación específica.

**POST /posts:** Crea una nueva publicación.

**DELETE /posts/{id_publicacion}:** Elimina una publicación existente.

**POST /posts/reset:** Restablece la base de datos, eliminando todos los datos.

**GET /posts/ping:** Consulta el estado de salud del servicio (ping).

## Pruebas Microservicio Publicaciones

Este repositorio contiene pruebas unitarias para el microservicio de publicaciones. Estas pruebas están diseñadas para evaluar las diversas funciones y rutas del microservicio y garantizar su correcto funcionamiento.

### Ejecución de las pruebas

Puede ejecutar las pruebas unitarias utilizando el siguiente comando: **python -m unittest discover tests**
Este comando buscará y ejecutará todas las pruebas en el directorio tests.

### Pruebas disponibles

**test_filtrar_publicaciones_expired_true**
Esta prueba verifica la funcionalidad de filtrar publicaciones con la bandera expire en true.

**test_filtrar_publicaciones_expired_false**
Esta prueba verifica la funcionalidad de filtrar publicaciones con la bandera expire en false.

**test_filtrar_publicaciones_invalid_expire_param**
Esta prueba verifica el manejo de un valor inválido para el parámetro expire al filtrar publicaciones.
**test_create_publicacion**
Esta prueba verifica la creación exitosa de una nueva publicación.

**test_create_sin_routeIs**
Esta prueba verifica la creación de una publicación sin proporcionar el campo routeId.

**test_create_post_sin_expireAt**
Esta prueba verifica la creación de una publicación sin proporcionar el campo expireAt.

**test_create_post_fecha_pasada**
Esta prueba verifica la creación de una publicación con una fecha de expiración en el pasado.

**test_route_id_invalid_type**
Esta prueba verifica el manejo de un valor incorrecto para el campo routeId.

**test_expire_at_invalid_date**
Esta prueba verifica el manejo de una fecha de expiración inválida en el campo expireAt.

**test_expire_at_expired_date**
Esta prueba verifica el manejo de una fecha de expiración en el pasado en el campo expireAt.

**test_create_publicacion_success**
Esta prueba verifica la creación exitosa de una nueva publicación con datos válidos.

**test_create_publicacion_error**
Esta prueba verifica el manejo de un error al crear una publicación debido a datos inválidos.

**test_consultar_publicacion_success**
Esta prueba verifica la consulta exitosa de una publicación por su ID.

**test_consultar_publicacion_invalid_id_format**
Esta prueba verifica el manejo de una solicitud de consulta de una publicación con un ID no válido.

**test_eliminar_publicacion**
Esta prueba verifica la eliminación exitosa de una publicación por su ID.

**test_eliminar_publicacion_invalid_id_format**
Esta prueba verifica el manejo de una solicitud de eliminación de una publicación con un ID no válido.

**test_reestablecer_basededatos_success**
Esta prueba verifica la restauración exitosa de la base de datos, eliminando todos los datos de prueba.

**test_ping**
Esta prueba verifica la disponibilidad del servicio a través de una solicitud de ping.
