# Microservicio de Usuarios

Este es un microservicio que gestiona los usuarios.

## Requisitos previos

Asegúrate de tener instalado:

    Python (versión 3.9)
    Docker
    Dependencias (ver requirements.txt)

## Instalación

    Clona este repositorio: git clone https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo6
    Accede a la carpeta del proyecto: cd Routes
    Crea un entorno virtual: python -m venv venv
    Activa el entorno virtual: source venv/bin/activate
    Instala las dependencias: pip install -r requirements.txt

## Dependencias que se instalaran

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

## Uso

Para correr localhost cambie la variables en el archivo

- DB_USER=postgres
- DB_PASSWORD=LosAndes1234
- DB_HOST=postgres-usuario
- DB_PORT=5433
- DB_NAME=users
- USERS_PATH=<http://usuario-app:3000>
- DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

  corra en consola con python app.py

- Para test debe estar la carpeta users
  modifica la cadena de conexion en la clase config que esta en la raiz de la carpeta users
  ![Alt text](image.png)
  Ejecuta el comando python -m unittest discover tests

## Estructura de Directorios

```
|—— .coverage
|—— .env
|—— app
|    |—— models
|        |—— usuario.py
|        |—— __init__.py
|        |—— __pycache__
|            |—— trayecto.cpython-311.pyc
|            |—— usuario.cpython-311.pyc
|            |—— __init__.cpython-311.pyc
|    |—— routes
|        |—— usuario_Routes.py
|        |—— __pycache__
|            |—— trayecto_Routes.cpython-311.pyc
|            |—— usuario_Routes.cpython-311.pyc
|    |—— __init__.py
|    |—— __pycache__
|        |—— __init__.cpython-311.pyc
|—— app.py
|—— config.py
|—— Dockerfile
|—— requirements.txt
|—— tests
|    |—— test_config.py
|    |—— test_usuario.py
|    |—— __init__.py
|    |—— __pycache__
|        |—— test_config.cpython-311.pyc
|        |—— test_trayecto.cpython-311.pyc
|        |—— test_usuario.cpython-311.pyc
|        |—— __init__.cpython-311.pyc
|—— __pycache__
|    |—— config.cpython-311.pyc
```

## Detalles de codigo

### Platforma de pruebas

- software
  ```
  OS: Debian unstable (May 2021), Ubuntu LTS
  Python: 3.8.5 (anaconda)
  PyTorch: 1.7.1, 1.8.1
  ```
- hardware
  ```
  CPU: Intel Xeon 6226R
  GPU: Nvidia RTX3090 (24GB)
  ```

## Referencias

- [Historia de usuario](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314/wiki/Gesti%C3%B3n-de-Usuarios)
- [Repositorio de codigo de users](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo6/tree/main/Users)
- [Repositorio de codigo de proyecto](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo6/)

## Ejecucion en docker

Ejecuta los siguientes comandos sobre la raiz del proyecto:

- docker-compose down
- docker-compose build
- docker-compose up -d
