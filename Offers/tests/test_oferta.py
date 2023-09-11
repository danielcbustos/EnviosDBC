import unittest
import json
from unittest.mock import patch
import uuid
from app import create_app, db
from app.models.oferta import Oferta
from faker import Faker
from datetime import timedelta

class OfertaOffersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()


    def test_create_oferta(self):
        fake = Faker()       
        oferta = Oferta(  
            
            postId="244b1ba6-0968-4a8b-86a1-e258b200cc0f",            
            description=fake.word(),
            size=fake.random_element(["LARGE","MEDIUM","SMALL"]),
            fragile=fake.pybool(),
            offer=fake.random_int(min=10000, max=1000000),
            createdAt=fake.date_time_this_decade()
        )
        db.session.add(oferta)
        db.session.commit()
        return oferta
    
    
    @patch('requests.get')
    def test_obtener_ofertas(self, mock_get):
       
        self.test_create_oferta() 
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200  
        response = self.client.get(
            "/offers",
            headers=headers
        )
        data = json.loads(response.data.decode())

        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)       
   
    @patch('requests.get')
    def test_crear_oferta(self, mock_get):
        fake = Faker()
        created_at = fake.date_time_this_decade()
        data = {
            "postId": "27d61c90-aee6-474f-b3b2-1981fe8d59a1",           
            "description": "la mejor oferta",
            "size": "LARGE",
            "fragile": True,
            "offer": 50000,
            "createdAt":f"{created_at}",
        }  

        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}        
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": token,            
        }

        response = self.client.post('/offers', json=data, headers = headers)
        data = json.loads(response.data.decode())      

        self.assertEqual(response.status_code, 201)       
      
        return response
 

    @patch('requests.get')
    def test_consultar_oferta_por_id_existente(self, mock_get):
        oferta=self.test_create_oferta()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200        
        response = self.client.get(f'/offers/{str(oferta.id)}',headers=headers)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['id'], str(oferta.id))

        #Consultar oferta no existente
        response = self.client.get(f'/offers/a24039d0-7b9b-4289-894d-ca7bd0bc8bdd',headers=headers)
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertEqual(data['msg'], "La oferta con ese id no existe")

        #Consultar oferta formato invalido uuid
        response = self.client.get(f'/offers/12345678',headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["msg"], "El id no es un valor string con formato uuid")
    
    @patch('requests.get')
    def test_eliminar_oferta(self, mock_get):
        oferta=self.test_create_oferta() 
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200            
      
        response = self.client.delete('/offers/' + str(oferta.id), headers=headers)

        self.assertEqual(response.status_code, 200)       
        data = json.loads(response.data.decode())
        self.assertEqual(data["msg"], "la oferta fue eliminada")

        #Eliminar oferta inexistente/ formato valido
        response = self.client.delete('/offers/41058b2b-8361-43d8-bf6f-7678cbd8e500',headers=headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["msg"], "La oferta con ese id no existe")

        #Eliminar oferta formato invalido uuid
        response = self.client.delete('/offers/123456',headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["msg"], "El id no es un valor string con formato uuid")
    
    @patch('requests.get')
    def test_filtrar_ofertas(self,mock_get):
        self.test_create_oferta()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}        
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": token,            
        }

        # Obtener las ofertas filtradas
        response = self.client.get('/offers?postId=244b1ba6-0968-4a8b-86a1-e258b200cc0f&owner=me', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

        ## postId tiene un formato uuid invalido
        response = self.client.get('/offers?postId=1243546&owner=me', headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["msg"], "El campo postId debe ser tipo UUID")

        ## userId tiene un formato uuid invalido
        response = self.client.get('/offers?postId=244b1ba6-0968-4a8b-86a1-e258b200cc0f&owner=136456', headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["msg"], "El campo userId debe ser 'me' o tipo UUID")

    def test_reestablecer_basededatos(self):     
        self.test_crear_oferta      
        response = self.client.post('/offers/reset')
        self.assertEqual(response.status_code, 200)

    def test_ping(self):        
        response = self.client.get("/offers/ping")        
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
