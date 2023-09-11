from app import db
import uuid
from datetime import datetime


class Usuarios(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()), nullable=False)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    dni = db.Column(db.String)
    fullName = db.Column(db.String)
    phoneNumber = db.Column(db.String)
    status = db.Column(db.String)
    createdAt = db.Column(
        db.DateTime, default=lambda: datetime.utcnow(), nullable=False)

    expiration_date = db.Column(
        db.DateTime, default=lambda: datetime.utcnow(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "dni": self.dni,
            "fullName": self.fullName,
            "phoneNumber": self.phoneNumber,  # ,
            "createdAt": self.createdAt.isoformat(),
            "expiration_date": self.expiration_date

        }
