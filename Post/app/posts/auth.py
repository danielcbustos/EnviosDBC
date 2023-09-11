# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# from functools import wraps
# from flask import request, jsonify
# #jwt = JWTManager(app)
# def require_token(func):
#     @wraps(func)
#     @jwt_required
#     def decorated(*args, **kwargs):
#         return func(*args, **kwargs)
#     return decorated

# @app.route('/login', methods=['POST'])
# def login():
#     # Aquí deberías tener la lógica para autenticar al usuario y verificar las credenciales.
#     # Si las credenciales son válidas, puedes generar y devolver un token de acceso.

#     # Ejemplo: Supongamos que el usuario se autenticó correctamente y tenemos su ID.
#     user_id = 1

#     # Crear un token de acceso con el ID del usuario
#     access_token = create_access_token(identity=user_id)

#     return jsonify(access_token=access_token), 200

# @app.route('/protected', methods=['GET'])
# @require_token
# def protected_route():
#     # Si llega a esta función, significa que el token es válido y el usuario está autenticado.
#     current_user_id = get_jwt_identity()
#     return jsonify(message=f"Usuario autenticado: {current_user_id}"), 200
