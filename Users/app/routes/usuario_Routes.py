from flask import request, jsonify, Blueprint
import jwt
from sqlalchemy import and_, or_
from app.models.usuario import Usuarios, db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


from datetime import datetime, timedelta

usuario_bp = Blueprint("usuario", __name__, url_prefix="/users")


@usuario_bp.route('/', methods=['POST'])
def Creacion_Usuario():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        dni = data.get("dni")
        phoneNumber = data.get("phoneNumber")
        fullName = data.get("fullName")

        userExiste = Usuarios.query.filter(
            or_(Usuarios.username == username,  Usuarios.email == email)).all()

        if ((username or password) or email) == False:
            return jsonify({}), 400
        if ((len(username) == 0 or len(password) == 0) or len(email) == 0):
            return jsonify({}), 400

        if len(userExiste) > 0:
            return jsonify({}), 412

        nuevo_usuario = Usuarios(
            username=username,
            password=password,
            email=email,
            dni=dni,
            phoneNumber=phoneNumber,
            fullName=fullName
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(
            {
                "id": nuevo_usuario.id,
                "createdAt": nuevo_usuario.createdAt.isoformat()
            }

        ), 201
    except Exception as e:
        return jsonify({}), 400

# Actualización de usuarios


@usuario_bp.route('/<string:id>', methods=['PATCH'])
def actualizar_usuarios(id):
    # id = request.args.get('id')
    data = request.json
    usuario = Usuarios.query.filter(
        (Usuarios.id == id)).first()

    if len(id) == 0:
        return jsonify({}), 400
    if usuario == None:
        return jsonify({}), 404

    required_fields = ["dni", "phoneNumber", "fullName", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({}), 400

    usuario.dni = data.get("dni")
    usuario.phoneNumber = data.get("phoneNumber")
    usuario.fullName = data.get("fullName")
    usuario.status = data.get("status")
    db.session.commit()
    return jsonify({
        "msg": "el usuario ha sido actualizado"
    }), 200


@usuario_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({}), 200


# Metodo para probar login


@usuario_bp.route("/auth", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    required_fields = ["username",   "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({}), 400

    usuario = Usuarios.query.filter(
        and_(Usuarios.username == username, Usuarios.password == password)).first()
    if usuario == None:
        return jsonify({}), 404
    user_id = usuario.id
    current_time = datetime.utcnow()

    # Sumar 1 hora a la fecha actual
    one_hour_later = current_time + timedelta(hours=1)

    # Convertir la fecha en formato ISO
    iso_format = one_hour_later.isoformat()

    usuario.expiration_date = one_hour_later
    db.session.commit()
    # expires_delta = timedelta(hours=1)
    # access_token = create_access_token(
    #     identity=user_id,  expires_delta=expires_delta)
    return jsonify({
        "id": user_id,
        "token": user_id,
        "expireAt": iso_format
    }), 200


#
@usuario_bp.route("/me", methods=["GET"])
def consultar_usuario():
    try:
        # Obtener el ID del usuario desde el token

        # Obtener el token del encabezado Authorization
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return jsonify({}), 403

        token = authorization_header.split(' ')[1]
        if len(token) == 0:
            return jsonify({

            }), 403

        # # Clave secreta utilizada para decodificar el token (reemplaza 'your_secret_key' con tu clave real)
        # secret_key = 'frase-secreta'

        # # Decodificar el token
        # decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

        # # Obtener la fecha de expiración del token
        # expiration_timestamp = decoded_token.get('exp')
        # expiration_date = datetime.utcfromtimestamp(expiration_timestamp)
        # current_time = datetime.now()
        # if (expiration_date < current_time):
        #     return jsonify({

        #     }), 404




        usuario = Usuarios.query.filter(
            (Usuarios.id == token)).first()
        
        
        if usuario == None:
            return jsonify({}), 401
        
        if usuario.expiration_date < datetime.utcnow():
            return jsonify({}), 403

        return jsonify(
            {
                "id": usuario.id,
                "username": usuario.username,
                "email": usuario.email,
                "fullName": usuario.fullName,
                "dni": usuario.dni,
                "phoneNumber": usuario.phoneNumber,
                "status": usuario.status
            }
        )
    except jwt.ExpiredSignatureError:
        return jsonify({}), 404
    except jwt.InvalidTokenError:
        return jsonify({}), 401


@usuario_bp.route('/reset', methods=['POST'])
def restablecer_usuarios():
    try:
        # Eliminar todos los datos de la tabla
        db.session.query(Usuarios).delete()
        db.session.commit()

        return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
    except Exception as e:

        return jsonify({}), 400
