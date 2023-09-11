from flask import request, jsonify, Blueprint
from app import db
from app.models.publicacion import Publicacion
#from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
import uuid
import requests
import os
import  json


publicacion_bp = Blueprint("publicacion", __name__, url_prefix="/posts")

def validarToken(token, response = False):
    parts = token.split()

    if len(parts) == 2 and parts[0] == 'Bearer':
        token1 = parts[1]
        

        url = f"{os.environ.get('USERS_PATH')}/users/me"
        headers = {'Authorization': f'Bearer {token1}'}
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            data = response.json()
            return data
        
        if response.status_code == 200:
            return True
        else:
            return False

#Filtrar y ver publicaciones
@publicacion_bp.route('', methods=['GET'])
#@jwt_required()
def filtrar_Publicaciones():
    route_id=None
    user_id=None
    expired = None
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not (token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id= token_valido["id"]
    else:
        return jsonify({"msg":"Token no encontrado"}), 403    

    #Validacion campo de busqueda
    if request.args.get('expire'):
        expired = request.args.get('expire')
        if expired not in ['true', 'false']:
            return jsonify({"msg": "El campo expire debe ser 'true', 'false' "}), 400
    
    if request.args.get('route'):
        route_id = request.args.get('route')    
        if route_id and not (isinstance(route_id, str)):
            return jsonify({"msg": "El campo route debe ser tipo str "}), 400

    if request.args.get('owner'):
        owner = request.args.get('owner')
        if owner != "me":
            user_id=request.args.get('owner')
        
    else:
        if user_id and not (user_id == 'me' or (isinstance(user_id, str) )):
            return jsonify({"msg": "El campo owner debe ser 'me' o tipo str"}), 400
         
    filtro=Publicacion.query
    if expired == 'true' and expired is not None:
        filtro = filtro.filter(Publicacion.expireAt < datetime.utcnow())
    elif expired == 'false' and expired is not None:
        filtro = filtro.filter(Publicacion.expireAt >= datetime.utcnow())
        
    if route_id is not None:
        filtro = filtro.filter(Publicacion.routeId==route_id)

    if user_id == 'me':
        filtro = filtro.filter(Publicacion.userId==user_id)
    elif user_id:
        filtro = filtro.filter(Publicacion.userId==user_id)
    
        
    publicaciones = filtro.all()
    publicaciones_data = []
    for publicacion in publicaciones:
        publicaciones_data.append({
            "id": publicacion.id,
            "routeId": publicacion.routeId, 
            "userId": publicacion.userId,
            "expireAt": publicacion.expireAt.isoformat(),
            "createdAt": publicacion.createdAt.isoformat(),
            
        })

    return jsonify(publicaciones_data), 200

#Metodo para poder consultar una publicacion 
@publicacion_bp.route('<string:id_publicacion>', methods=['GET'])
#@jwt_required()
def consultar_Publicacion(id_publicacion):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
    else:
        return jsonify({"msg":"Token no encontrado"}), 403    
   
    try:
        # Id formato uuid      
        if not uuid.UUID(id_publicacion):
                return None
        publicacion=Publicacion.query.get(id_publicacion)
        #id existente
        if publicacion is None:
            return jsonify({"msg": "La publicacion con ese id no existe"}), 404       
    except Exception as e:
        return jsonify({"msg": "El id no es un valor string con formato uuid"}), 400
    
    publicacion_data={
            "id": publicacion.id,
            "routeId": publicacion.routeId, 
            "userId": publicacion.userId,
            "expireAt": publicacion.expireAt.isoformat(),
            "createdAt": publicacion.createdAt.isoformat(),
        }

    return jsonify(publicacion_data), 200


# Ruta para crear una publicación
@publicacion_bp.route('', methods=['POST'])
#@jwt_required()
def create_publicacion():
    
    authorization_header = request.headers.get('Authorization')
    user_id=""
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not (token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id= token_valido["id"]
    else:
        return jsonify({"msg":"Token no encontrado"}), 403    
    data = request.json



    # Validacion tipos de datos correctos

    #Todos los campos son requeridos --->400
    
    required_fields = ['routeId', 'expireAt']
    for field in required_fields:

        if field not in data:
            return jsonify({"msg": f"Falta el campo obligatorio: {field}"}), 400
    route_id = data.get('routeId')
    expire_at = data.get('expireAt')    
    # Validacion tipos de datos correctos
        
    if not isinstance(data['routeId'], str):
        return jsonify({"msg": "El campo routeid debe ser tipo String"}), 400

   
    publicacion_existe = Publicacion.query.filter_by(routeId=route_id).first()
    #if publicacion_existe:
        #return jsonify(), 412 

    try:
        expire_at_iso = data.get('expireAt')
        expire_at = datetime.fromisoformat(expire_at_iso[:-1] if expire_at_iso.endswith('Z') else expire_at_iso)
        if expire_at < datetime.utcnow() :
            return jsonify({"msg": "La fecha expiración no es válida"}), 412
    except Exception as e:
        return jsonify({"msg": f"La fecha expiración no es válida"}), 412
    

    try:
        # print("eeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        # print(user_id)
        nueva_publicacion = Publicacion(
            userId =user_id,
            routeId=route_id,
            expireAt=expire_at
        )

        db.session.add(nueva_publicacion)
        db.session.commit()
        response_data = {
            "id": nueva_publicacion.id,
            "userId": nueva_publicacion.userId,
            "createdAt": nueva_publicacion.createdAt
    }
        
        print(response_data)
        return jsonify(response_data), 201
    except Exception as e:
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        print(str(e))
        return jsonify({"msg": "Error al crear la publicación", "error": str(e)}), 500    
    
#Eliminar una publicación  
@publicacion_bp.route('<string:id_publicacion>', methods=['DELETE'])
#@jwt_required()
def eliminar_publicacion(id_publicacion):
    authorization_header = request.headers.get('Authorization')

    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401

    else:
        return jsonify({"msg":"Token no encontrado"}), 403

    # Id formato uuid      
    
    try:   
        if not uuid.UUID(id_publicacion):
            return None
        publicacion=Publicacion.query.get(id_publicacion)
        if publicacion is None:
            return jsonify(),404
        db.session.delete(publicacion)
        db.session.commit()
        return jsonify({"msg": "la publicación fue eliminada"}), 200 

    except Exception as e:    
            return jsonify(), 400    
    





#Reestablecer base de datos
@publicacion_bp.route('/reset', methods=['POST'])
def reestablecer_basededatos():
    try:       
        Publicacion.query.delete()
        db.session.commit()

        return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

#Consultar estado de salud de un servicio Ping
@publicacion_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({}), 200 


