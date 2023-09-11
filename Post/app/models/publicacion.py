from app import db
from sqlalchemy import UniqueConstraint
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Publicacion(db.Model):
    id = db.Column(db.String, primary_key=True,unique=True, default=lambda:str(uuid.uuid4()), nullable=False)
    routeId = db.Column(db.String, nullable=False)
    userId = db.Column(db.String)
    expireAt = db.Column(db.DateTime, default=lambda:datetime.utcnow(),nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda:datetime.utcnow(), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "routeId": self.routeId,
            "userId": self.userId,
            "expireAt": self.expireAt.isoformat(),
            "createAt": self.expireAt.isoformat(),
      
        }
