import unittest
import json
from app import create_app, db
from app.models.usuario import Usuarios
from flask_jwt_extended import create_access_token, JWTManager
from faker import Faker
from datetime import timedelta


class UsuarioRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        with self.app.app_context():
            jwt = JWTManager(self.app)
            db.create_all()
            self.usuarioDefault()

        # Definimos los endpoints para las pruebas y el header necesario para las peticiones
        self.endpoint_user = "/users"

        self.client = self.app.test_client()

    # Consultar de informacion

    def test_ConsultaInformacionDatosValidos(self):

        login = {
            "username": self.username,
            "password": self.password
        }
        solicitud_login = self.client.post("/users/auth",
                                           data=json.dumps(login),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())
        token = respuesta_login["token"]

        headersToken = {'Content-Type': 'application/json',
                        "Authorization": "Bearer {}".format(token)}

        solicitud_username = self.client.get(
            "/users/me", headers=headersToken)
        datos_username = json.loads(solicitud_username.get_data())

        self.assertEqual(self.email, datos_username["email"])
        self.assertEqual(self.username, datos_username["username"])
        self.assertEqual(self.fullName, datos_username["fullName"])
        self.assertEqual(solicitud_login.status_code, 200)

    def test_ConsultaInformacionDatosValidosNoToken(self):

        solicitud_username = self.client.get(
            "/users/me", headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_username.status_code, 403)

    # Metodo creacion  Usuario

    def test_CreacionUsuarioDatosValidos(self):
        username = "usr"+str(self.data_factory.random_number())
        password = 'T1$' + self.data_factory.word()
        email = self.data_factory.email()
        dni = str(self.data_factory.random_number())
        phoneNumber = str(self.data_factory.random_number())
        fullName = self.data_factory.name()
        nuevo_usuario = {
            "username": username,
            "password": password,
            "email": email,
            "dni": dni,
            "phoneNumber": phoneNumber,
            "fullName": fullName
        }

        solicitud_login = self.client.post("/users/",
                                           data=json.dumps(nuevo_usuario),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 201)

    def test_CreacionUsuarioDatosPreexistentes(self):
        username = self.username
        password = 'T1$' + self.data_factory.word()
        email = self.data_factory.email()
        dni = str(self.data_factory.random_number())
        phoneNumber = str(self.data_factory.random_number())
        fullName = self.data_factory.name()

        nuevo_usuario = {
            "username": username,
            "password": password,
            "email": email,
            "dni": dni,
            "phoneNumber": phoneNumber,
            "fullName": fullName
        }

        solicitud_login = self.client.post("/users/",
                                           data=json.dumps(nuevo_usuario),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 412)

    def test_CreacionUsuarioSinTodosCampos(self):

        username = ""
        password = 'T1$' + self.data_factory.word()
        email = self.data_factory.email()
        dni = str(self.data_factory.random_number())
        phoneNumber = str(self.data_factory.random_number())
        fullName = self.data_factory.name()

        nuevo_usuario = {
            "username": username,
            "email": email,
            "dni": dni,
            "phoneNumber": phoneNumber,
            "fullName": fullName
        }

        solicitud_login = self.client.post("/users/",
                                           data=json.dumps(nuevo_usuario),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 400)

    # Metodo Actualización de usuarios

    def test_Actualizacion_UsuariosDatosCorrectos(self):
        campoActualizacion = {
            "status": self.data_factory.word(),
            "dni": str(self.data_factory.random_number()),
            "fullName": self.data_factory.name(),
            "phoneNumber": str(self.data_factory.random_number())
        }

        solicitud_login = self.client.patch("/users/" + str(self.id),
                                            data=json.dumps(
            campoActualizacion),
            headers={'Content-Type': 'application/json'})

        self.assertEqual(solicitud_login.status_code, 200)

    # Metodo  Generación de token

    def test_GeneracionTokenDatosValidos(self):
        login = {
            "username": self.username,
            "password": self.password
        }
        solicitud_login = self.client.post("/users/auth",
                                           data=json.dumps(login),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 200)

    def test_GeneracionTokenDatosUsuarioNoExiste(self):
        self.usrFake = "usr" + str(self.data_factory.random_number())
        login = {
            "username": self.usrFake,
            "password": self.password
        }
        solicitud_login = self.client.post("/users/auth",
                                           data=json.dumps(login),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 404)

    def test_GeneracionTokenDatosUsuarioCampoNoPresente(self):
        self.usrFake = "usr" + str(self.data_factory.random_number())
        login = {

            "password": self.password
        }
        solicitud_login = self.client.post("/users/auth",
                                           data=json.dumps(login),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 400)

    def test_GeneracionTokenDatosFaltaCampo(self):

        login = {

            "password": self.password
        }
        solicitud_login = self.client.post("/users/auth",
                                           data=json.dumps(login),
                                           headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())

        self.assertEqual(solicitud_login.status_code, 400)

    def usuarioDefault(self):
        self.data_factory = Faker()
        self.username = "usr"+str(self.data_factory.random_number())
        self.password = 'T1$' + self.data_factory.word()
        self.email = self.data_factory.email()
        self.dni = str(self.data_factory.random_number())
        self.phoneNumber = str(self.data_factory.random_number())
        self.fullName = self.data_factory.name()
    # Crea la aplicación de prueba

        nuevo_usuario = Usuarios(
            username=self.username,
            password=self.password,
            email=self.email,
            dni=self.dni,
            phoneNumber=self.phoneNumber,
            fullName=self.fullName
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        self.id = nuevo_usuario.id

    def test_ping_endpoint(self):
        response = self.client.get(
            "/users/ping", headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    if __name__ == "__main__":
        unittest.main()
