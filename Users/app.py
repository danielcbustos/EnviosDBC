from app import create_app,db 
from flask_jwt_extended import JWTManager
from flask import jsonify
app = create_app()

# Crear la base de datos si no existe
with app.app_context():
   db.create_all()
   
   #jwt= JWTManager(app)
   # @jwt.unauthorized_loader
   # def unauthorized_response_callback(error):
   #    return jsonify({}), 403

   # @jwt.invalid_token_loader
   # def invalid_token_response_callback(error):
   #    return jsonify({}), 401
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
