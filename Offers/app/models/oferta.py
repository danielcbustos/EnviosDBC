from app import db
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Oferta(db.Model):
    id = db.Column(db.String, primary_key=True,unique=True, default=lambda:str(uuid.uuid4()), nullable=False )     
    postId = db.Column(db.String, nullable=False)
    userId = db.Column(db.String)
    description = db.Column(db.String(140), nullable=False)
    size = db.Column(db.String,Enum("LARGE", "MEDIUM", "SMALL", name="size_enum"), nullable=False)
    fragile = db.Column(db.Boolean, nullable=False)
    offer = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda:datetime.utcnow(), nullable=False) 

    def to_dict(self):
        return {
            "id": self.id,
            "postId": self.postId,
            "userId": self.userId,
            "description": self.description,
            "size": self.size,
            "fragile": self.fragile,
            "offer": self.offer,
            "createdAt": self.createdAt
        }



  
    
         
      
