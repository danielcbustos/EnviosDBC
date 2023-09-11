# Microservicio de Ofertas

Este microservicio permite gestionar ofertas en una plataforma. Proporciona funcionalidades para crear, consultar, filtrar y eliminar ofertas. A continuación, se detallan los pasos para configurar, instalar y ejecutar el microservicio, así como también cómo usar Docker para facilitar el proceso.

## Requisitos previos

Asegúrate de tener instalado:

- Python (versión 3.9)
- Docker
- Dependencias (ver [requirements.txt](requirements.txt))

## Instalación

1. Clona este repositorio: `git clone https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo6`
2. Accede a la carpeta del proyecto: `cd Offers`
3. Crea un entorno virtual: `python -m venv venv`
4. Activa el entorno virtual: `source venv/bin/activate`
5. Instala las dependencias: `pip install -r requirements.txt`

## Ejecución

### Ejecutar el microservicio

1. Asegúrate de que las variables de entorno están configuradas correctamente.
2. Desde la raíz del proyecto, ejecuta: `python app.py`

### Ejecutar con Docker Compose

1. Asegúrate de que las variables de entorno están configuradas correctamente en el archivo `.env`.
2. Desde la raíz del proyecto, ejecuta: `docker-compose up`

### Ejecutar directamente con Dockerfile

1. Asegúrate de que las variables de entorno están configuradas correctamente en el archivo `.env`.
2. Construye la imagen Docker: `docker build -t oferta-app .`
3. Ejecuta el contenedor con la imagen creada: `docker run -p 3003:3003 -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e DB_HOST=$DB_HOST -e DB_PORT=$DB_PORT -e DB_NAME=$DB_NAME -e USERS_PATH=$USERS_PATH oferta-app`

**Nota:** Asegúrate de reemplazar `$DB_USER`, `$DB_PASSWORD`, `$DB_HOST`, `$DB_PORT`, `$DB_NAME` y `$USERS_PATH` con los valores reales correspondientes en tu entorno.

## Uso

Una vez que el microservicio esté en funcionamiento, puedes interactuar con él mediante una API REST.

- Crear una oferta: `POST /offers`
- Consultar oferta por ID: `GET /offers/<id>`
- Eliminar oferta por ID: `DELETE /offers/<id>`
- Filtrar ofertas: `GET /offers?postId=<postId>&owner=<owner>`

## Pruebas

Para ejecutar las pruebas unitarias, asegúrate de tener el entorno virtual activado y las dependencias instaladas. Luego, desde la raíz del proyecto, ejecuta:

python -m unittest discover tests
