from app import create_app,db 
from flask_jwt_extended import JWTManager
from flask import jsonify
app = create_app()

# Crear la base de datos si no existe
with app.app_context():
   db.create_all()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
