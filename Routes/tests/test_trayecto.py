import unittest
import json
import uuid
from app import create_app, db
from app.models.trayecto import Trayecto
from faker import Faker
from datetime import timedelta
from unittest.mock import patch

class TrayectoRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    
    def create_test_trayecto(self):
        fake = Faker()
        planned_start_date = fake.future_datetime()
        planned_end_date = planned_start_date + timedelta(minutes=fake.random_int(min=30, max=120))

        trayecto = Trayecto(
            flightId=fake.unique.word(),
            sourceAirportCode=fake.unique.word(),
            sourceCountry=fake.country(),
            destinyAirportCode=fake.unique.word(),
            destinyCountry=fake.country(),
            bagCost=fake.random_int(min=10, max=100),
            plannedStartDate=planned_start_date,
            plannedEndDate=planned_end_date,
            createdAt=fake.date_time_this_decade()
        )
        db.session.add(trayecto)
        db.session.commit()
        return trayecto
    
    @patch('requests.get')
    def test_obtener_trayectos(self, mock_get):
        # Arrange 
        self.create_test_trayecto()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        # Act
        response = self.client.get(
            "/routes",
            headers=headers
        )
        data = json.loads(response.data.decode())

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    @patch('requests.get')
    def test_crear_trayecto(self, mock_get):
        # Arrange
        fake = Faker()
        planned_start_date = fake.future_datetime()
        planned_end_date = planned_start_date + timedelta(minutes=fake.random_int(min=30, max=120))
        data = {
            "flightId": "AA001",
            "sourceAirportCode": "ABC",
            "sourceCountry": "Country A",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "Country B",
            "bagCost": 50,
            "plannedStartDate": f"{planned_start_date}",
            "plannedEndDate": f"{planned_end_date}",
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200
        # Act
        response = self.client.post("/routes", json=data, headers = headers)
        data = json.loads(response.data.decode())

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertIn("createdAt", data)

    def test_ping(self):
         #Act
        response = self.client.get(
            "/routes/ping"
        )

        #Assert
        self.assertEqual(response.status_code, 200)

    # # def test_obtener_trayecto(self):
    # #     # Arrange 
    # #     trayecto = self.create_test_trayecto()
    # #     token = self.get_jwt_token()
    # #     headers = {"Authorization": f"Bearer {token}"}

    # #     # Act
    # #     response = self.client.get(
    # #         f"routes/{trayecto.id}",
    # #         headers=headers
    # #     )
    # #     data = json.loads(response.data.decode())
    # #     #Assert
    # #     self.assertEqual(response.status_code, 200)
    # #     self.assertEqual(data["id"], trayecto.id)
    # #     self.assertEqual(data["flightId"], trayecto.flightId)
    # #     self.assertEqual(data["sourceAirportCode"], trayecto.sourceAirportCode)
    # #     self.assertEqual(data["sourceCountry"], trayecto.sourceCountry)
    # #     self.assertEqual(data["destinyAirportCode"], trayecto.destinyAirportCode)
    # #     self.assertEqual(data["destinyCountry"], trayecto.destinyCountry)
    # #     self.assertEqual(data["bagCost"], trayecto.bagCost)

    @patch('requests.get')
    def test_eliminar_trayecto(self, mock_get):
        # Arrange 
        trayecto = self.create_test_trayecto()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.delete(
            f"routes/{trayecto.id}",
            headers=headers
        )
        #Assert
        self.assertEqual(response.status_code, 200)

    def test_reset_db(self):
        # Arrange
        self.create_test_trayecto()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}

        # Act
        response = self.client.post(
            f"routes/reset",
            headers=headers
        )
        #Assert
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_obtener_trayectos_filtrado(self, mock_get):
        # Arrange
        trayecto1 = self.create_test_trayecto()
        trayecto2 = self.create_test_trayecto()
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.get(
            f"routes?flight={trayecto1.flightId}",
            headers=headers
        )
        data = json.loads(response.data.decode())

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], trayecto1.id)
        self.assertEqual(data[0]["flightId"], trayecto1.flightId)
        self.assertEqual(data[0]["sourceAirportCode"], trayecto1.sourceAirportCode)
        self.assertEqual(data[0]["sourceCountry"], trayecto1.sourceCountry)
        self.assertEqual(data[0]["destinyAirportCode"], trayecto1.destinyAirportCode)
        self.assertEqual(data[0]["destinyCountry"], trayecto1.destinyCountry)
        self.assertEqual(data[0]["bagCost"], trayecto1.bagCost)

    @patch('requests.get')
    def test_crear_trayecto_incompleto(self, mock_get):
        # Arrange
        fake = Faker()
        planned_start_date = fake.future_datetime()
        planned_end_date = planned_start_date + timedelta(minutes=fake.random_int(min=30, max=120))
        data = {
            "flightId": "AA001",
            "sourceCountry": "Country A",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "Country B",
            "bagCost": 50,
            "plannedStartDate": f"{planned_start_date}",
            "plannedEndDate": f"{planned_end_date}",
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.post("/routes", json=data, headers = headers)
        data = json.loads(response.data.decode())

        # Assert
        self.assertEqual(response.status_code, 400)

    @patch('requests.get')
    def test_crear_trayecto_duplicado(self, mock_get):
        # Arrange
        trayecto = self.create_test_trayecto() 
        fake = Faker()
        planned_start_date = fake.future_datetime()
        planned_end_date = planned_start_date + timedelta(minutes=fake.random_int(min=30, max=120))
        data = {
            "flightId": f"{trayecto.flightId}",
            "sourceAirportCode": "ABC",
            "sourceCountry": "Country A",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "Country B",
            "bagCost": 50,
            "plannedStartDate": f"{planned_start_date}",
            "plannedEndDate": f"{planned_end_date}",
        }
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.post("/routes", json=data, headers = headers)

        # Assert
        self.assertEqual(response.status_code, 412)

    @patch('requests.get')
    def test_crear_trayecto_error_fechas(self, mock_get):
       # Arrange
       fake = Faker()
       planned_start_date = fake.future_datetime()
       planned_end_date = planned_start_date + timedelta(minutes=fake.random_int(min=30, max=120))
       data = {
           "flightId": "AA001",
           "sourceAirportCode": "ABC",
           "sourceCountry": "Country A",
           "destinyAirportCode": "XYZ",
           "destinyCountry": "Country B",
           "bagCost": 50,
           "plannedStartDate": f"{planned_end_date}",
           "plannedEndDate": f"{planned_start_date}",
       }
       token = str(uuid.uuid4())
       headers = {"Authorization": f"Bearer {token}"}
       mock_get.return_value.status_code = 200
       # Act
       response = self.client.post("/routes", json=data, headers = headers)
       data = json.loads(response.data.decode())
       # Assert
       self.assertEqual(response.status_code, 412)
       self.assertEqual(data["msg"], "Las fechas del trayecto no son válidas")

    @patch('requests.get')
    def test_obtener_trayecto_IdInvalido(self, mock_get):
        # Arrange
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.get(
            f"routes/1",
            headers=headers
        )
        #Assert
        self.assertEqual(response.status_code, 400)

    @patch('requests.get')
    def test_obtener_trayecto_NoExiste(self, mock_get):
        # Arrange
        token = str(uuid.uuid4())
        headers = {"Authorization": f"Bearer {token}"}
        mock_get.return_value.status_code = 200

        # Act
        response = self.client.get(
            f"routes/{str(uuid.uuid4())}",
            headers=headers
        )
        data = json.loads(response.data.decode())

        #Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["msg"], "El trayecto con ese id no existe")

if __name__ == "__main__":
    unittest.main()
