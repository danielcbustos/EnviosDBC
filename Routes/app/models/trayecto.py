from app import db
import uuid
from datetime import datetime

class Trayecto(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda:str(uuid.uuid4()), nullable=False)
    flightId = db.Column(db.String, unique=True, nullable=False)
    sourceAirportCode = db.Column(db.String, nullable=False)
    sourceCountry = db.Column(db.String, nullable=False)
    destinyAirportCode = db.Column(db.String, nullable=False)
    destinyCountry = db.Column(db.String, nullable=False)
    bagCost = db.Column(db.Integer, nullable=False)
    plannedStartDate = db.Column(db.DateTime, nullable=False)
    plannedEndDate = db.Column(db.DateTime, nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda:datetime.utcnow(), nullable=False)
    updatedAt = db.Column(db.DateTime, default=lambda:datetime.utcnow(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "flightId": self.flightId,
            "sourceAirportCode": self.sourceAirportCode,
            "sourceCountry": self.sourceCountry,
            "destinyAirportCode": self.destinyAirportCode,
            "destinyCountry": self.destinyCountry,
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate.isoformat(),
            "plannedEndDate": self.plannedEndDate.isoformat(),
            "createdAt": self.createdAt.isoformat(),
        }
