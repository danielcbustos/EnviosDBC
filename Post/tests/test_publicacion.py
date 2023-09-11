import unittest
import json
from app import create_app, db
from app.models.publicacion import Publicacion
from flask_jwt_extended import create_access_token, JWTManager
from faker import Faker
from sqlalchemy import text
from unittest.mock import patch
import uuid


class TestPublicacion(unittest.TestCase):
    def setUp(self):
        # Configura la aplicación para pruebas
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        # Crea un contexto de aplicación para interactuar con la base de datos
        with self.app.app_context():
            jwt = JWTManager(self.app)
            db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def get_jwt_token(self):
        # Genera un token JWT para las pruebas
        access_token = create_access_token(identity="1")
        return access_token
    


    
    def create_test_post(self,expired):
        try:

            fake = Faker()
            if expired:
                date = fake.past_datetime()
            else:
                date = fake.future_datetime()   
            post = Publicacion(routeId='1', expireAt=date)
            db.session.add(post)
            db.session.commit()
            return post
        except Exception as e:
            return {"msg": "El id no es un valor string con formato uuid","error":e}

      

    @patch('requests.get')
    def test_filtrar_publicaciones_expired_true(self, mock_get):
        # Crear una publicación expirada
        publicacion_expirada = self.create_test_post(True)
        # Solicitar publicaciones expiradas
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
             "id":publicacion_expirada.id,

        }

        response = self.client.get('/posts?expire=true',headers=headers)
        self.assertEqual(response.status_code, 200)
        #self.assertTrue(len(response.json) > 0)


    @patch('requests.get')
    def test_filtrar_publicaciones_expired_false(self, mock_get):
        # Crear una publicación futura
        publicacion_expirada=self.create_test_post(False)
        # Solicitar publicaciones no expiradas
        token = str(uuid.uuid4())
        mock_response = mock_get.return_value
        headers = {"Authorization": f"Bearer {token}"}
        mock_response.status_code = 200
        mock_response.json.return_value = {
             "id":publicacion_expirada.id,

        }

        response = self.client.get('/posts?expire=false',headers=headers)
        self.assertEqual(response.status_code, 200)
        
    
    @patch('requests.get')        
    def test_filtrar_publicaciones_invalid_expire_param(self, mock_get):
        # Solicitar publicaciones con un valor inválido para 'expire'
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.get('/posts?expire=invalid_value',headers=headers)
        self.assertEqual(response.status_code, 400)
 

    # # Pruebas para crear publicaciones  
    
    @patch('requests.get')           
    def test_create_publicacion(self, mock_get):
    # Prueba para crear una publicación válida
        fake = Faker()

        data = {
            'routeId': '1',
            'expireAt': f'{fake.future_datetime() }'
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        # print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        # print(headers)
        # print(token)
        # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        mock_get.return_value.status_code = 200
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id":token,

        }
        response = self.client.post('/posts', json=data,headers = headers)
        self.assertEqual(response.status_code, 201)

    #Prueba para crear una publicación sin proporcionar 'routeId'
    
    @patch('requests.get')
    def test_create_sin_routeIs(self, mock_get):
        fake = Faker()
        data_sin_routeId= {
            'expireAt': f'{fake.future_datetime() }'
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        response = self.client.post('/posts', json=data_sin_routeId,headers = headers)
        self.assertEqual(response.status_code, 400) 

    #Prueba para crear una publicación sin proporcionar 'expiteAt'
    @patch('requests.get')
    def test_create_post_sin_expireAt(self, mock_get):

        data_sin_expireAt= {
            'routeId': '1'
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.post('/posts', json=data_sin_expireAt, headers = headers)
        self.assertEqual(response.status_code, 400) 
    
    # Prueba para crear una publicación con una fecha de expiración en el pasado
    @patch('requests.get')
    def test_create_post_fecha_pasada(self, mock_get):
        fake = Faker()
        data_expired = {
            'routeId': 'example_route',
            'expireAt': f'{fake.past_datetime() }'
        }
        
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response_expired = self.client.post('/posts', json=data_expired, headers = headers)
        self.assertEqual(response_expired.status_code, 412)    


    @patch('requests.get') 
    def test_route_id_invalid_type(self,mock_get):
        fake = Faker()
        # Prueba para validar que 'routeId' debe ser una cadena
        data = {
            'routeId': 123,  # Debería ser una cadena, no un entero
            'expireAt': f'{fake.future_datetime() }'
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.post('/posts', json=data, headers = headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("El campo routeid debe ser tipo String", response.json['msg'])


    @patch('requests.get') 
    def test_expire_at_invalid_date(self,mock_get):
        # Prueba para validar que 'expireAt' debe ser una fecha válida en formato ISO
        data = {
            'routeId': '1',
            'expireAt': 2023-12-31  # Formato inválido 
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.post('/posts', json=data, headers = headers)
        self.assertEqual(response.status_code, 412)
        self.assertIn("La fecha expiración no es válida", response.json['msg'])

    @patch('requests.get')    
    def test_expire_at_expired_date(self,mock_get):
        fake = Faker()
        # Prueba para validar que 'expireAt' no puede ser una fecha en el pasado
        data = {
            'routeId': '1',
            'expireAt': f'{fake.past_datetime() }'  # Fecha en el pasado
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.post('/posts', json=data, headers = headers)
        self.assertEqual(response.status_code, 412)
        self.assertIn("La fecha expiración no es válida", response.json['msg'])
    

    # Prueba para crear nueva publicacion
    @patch('requests.get')  
    def test_create_publicacion_success(self,mock_get):
        fake = Faker()
        # Datos válidos para crear una publicación
        data = {
            'routeId': 'example_route',
            'expireAt': f'{fake.future_datetime() }'
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"id":token}
        response = self.client.post('/posts', json=data, headers = headers)
        self.assertEqual(response.status_code, 201)
     
        
        # Verificar que la respuesta contenga los datos de la nueva publicación
       
        self.assertIn("id", response.json)
        self.assertIn("userId", response.json)
        self.assertIn("createdAt", response.json)


    @patch('requests.get')  
    def test_create_publicacion_error(self,mock_get):
        # Datos inválidos para crear una publicación ( falta 'expireAt')
        data = {
            'routeId': 'example_route'
        }

        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.post('/posts', json=data, headers = headers)
        self.assertEqual(response.status_code, 400)


    #PRUEBAS PARA CONSULTAR PUBLICACION
    @patch('requests.get')  
    def test_consultar_publicacion_success(self,mock_get):
        # Crear una publicación de ejemplo en la base de datos
        publicacion = self.create_test_post(False)

        # Obtener el ID de la publicación recién creada
        publicacion_id = publicacion.id

        # Solicitar la consulta de la publicación por su ID
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.get(f'/posts/{publicacion_id}', headers = headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json)
        self.assertIn("routeId", response.json)
        self.assertIn("userId", response.json)
        self.assertIn("expireAt", response.json)
        self.assertIn("createdAt", response.json)

    @patch('requests.get')  
    def test_consultar_publicacion_invalid_id_format(self,mock_get):

        # Solicitar la consulta de una publicación con un ID no válido
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        response = self.client.get('/posts/invalid_id', headers = headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("El id no es un valor string con formato uuid", response.json['msg'])


    # PRUEBA PARA ELIMINAR PUBLICACION
    @patch('requests.get')  
    def test_eliminar_publicacion(self,mock_get):
        fake = Faker()
    # Crear una publicación de prueba
        Publicacion = self.create_test_post(False)

        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200  
        response_create = self.client.delete(f'/posts/{Publicacion.id}', headers = headers)
        self.assertEqual(response_create.status_code, 200)
       
  

    # Solicitar la eliminación de una publicación con un ID no válido
    @patch('requests.get')  
    def test_eliminar_publicacion_invalid_id_format(self,mock_get):

        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200  
        response = self.client.delete('/posts/invalid_id',headers = headers)
        self.assertEqual(response.status_code, 400)



    #PRUEBAS PARA REESTABLECER BASES DE DATOS  
    @patch('requests.get')    
    def test_reestablecer_basededatos_success(self,mock_get):
        # Crear algunas publicaciones de ejemplo en la base de datos
        publicacion1 = self.create_test_post(False)
        publicacion2 = self.create_test_post(False)

        # Solicitar la restauración de la base de datos

        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200  
        response = self.client.post('/posts/reset', headers = headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Todos los datos fueron eliminados", response.json['msg'])

        # Verificar que la base de datos esté vacía
        with self.app.app_context():
            publicaciones = Publicacion.query.all()
            self.assertEqual(len(publicaciones), 0)


    def test_ping(self):
         #Act
        response = self.client.get(
            "/posts/ping"
        )

        #Assert
        self.assertEqual(response.status_code, 200)