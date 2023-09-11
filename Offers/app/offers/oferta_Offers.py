import json
import os
from flask import request, jsonify, Blueprint
import requests
from app import db
from app.models.oferta import Oferta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
import uuid


oferta_bp = Blueprint("oferta", __name__, url_prefix="/offers")

def validarToken(token, response=False):
    parts = token.split()
    if len(parts) == 2 and parts[0] == 'Bearer':
        token1 = parts[1]

        url = f"{os.environ.get('USERS_PATH')}/users/me"       
        headers = {'Authorization': f'Bearer {token1}'}
        response = requests.get(url, headers=headers)
        if response and response.status_code==200:
            data = response.json()
            return data
        if response.status_code == 200:
            return True
        else:
            return False


#Filtrar y ver ofertas
@oferta_bp.route('', methods=['GET'])

def filtrar_Ofertas():
    authorization_header = request.headers.get('Authorization')
    user_id=""
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id=token_valido["id"]

    else:
        return jsonify({"msg":"Token no encontrado"}), 403
 
    #Validacion campo de busqueda
    try:
        post_id = request.args.get('postId')    
        if post_id and not (isinstance(post_id, str) and uuid.UUID(post_id, version=4)):
            return jsonify({"msg": "El campo postId debe ser tipo UUID "}), 400
    except Exception as e:
        return jsonify({"msg": "El campo postId debe ser tipo UUID", "error": str(e)}), 400

    try:   
        owner=request.args.get('owner')
        if owner and not (owner == 'me' or (isinstance(owner, str) and uuid.UUID(owner, version=4))):
            return jsonify({"msg": "El campo userId debe ser 'me' o tipo UUID"}), 400
    except Exception as e:    
            return jsonify({"msg": "El campo userId debe ser 'me' o tipo UUID", "error": str(e)}), 400
        
    filtro=Oferta.query
    if post_id:
        filtro = filtro.filter_by(postId=post_id)
    if owner == 'me':
        user_id_token = user_id
        filtro = filtro.filter_by(userId=user_id_token)
    elif owner:
        filtro = filtro.filter_by(userId=owner)
         

    ofertas = filtro.all()

    ofertas_data = []
    for oferta in ofertas:
        ofertas_data.append({
            "id": oferta.id,
            "postId": oferta.postId, 
            "description": oferta.description,
            "size": oferta.size,
            "fragile": oferta.fragile,
            "offer": oferta.offer,
            "createdAt": oferta.createdAt,
            "userId":oferta.userId
        })

    return jsonify(ofertas_data), 200

#Obtener oferta segun ofertaId
@oferta_bp.route('<string:id_oferta>', methods=['GET'])

def consultar_Oferta(id_oferta):   
    authorization_header = request.headers.get('Authorization')
    user_id=""
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id=token_valido["id"]
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    
    try:
        # Id formato uuid      
        if not uuid.UUID(id_oferta):
                return None
        oferta=Oferta.query.get(id_oferta)
        #id existente
        if oferta is None:
            return jsonify({"msg": "La oferta con ese id no existe"}), 404       
    except Exception as e:
        return jsonify({"msg": "El id no es un valor string con formato uuid"}), 400
    
    oferta_data={
            "id": oferta.id,
            "postId": oferta.postId,            
            "description": oferta.description,
            "size": oferta.size,
            "fragile": oferta.fragile,
            "offer": oferta.offer,
            "createdAt": oferta.createdAt.isoformat(),
            "userId": oferta.userId
        }
    

    return jsonify(oferta_data), 200

#Crear Oferta
@oferta_bp.route('', methods=['POST'])

def crear_oferta():
   
    authorization_header = request.headers.get('Authorization')
    user_id=""
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id=token_valido["id"]
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    
    data = request.json

    post_id = data.get('postId')    
    description = data.get('description')
    size = data.get('size')
    fragile = data.get('fragile')
    offer = data.get('offer')

    try:

        #Todos los campos son requeridos --->400
        required_fields = ["postId", "description", "size", "fragile", "offer"]
        for field in required_fields:
            if field not in data:
                return jsonify({"msg": f"Falta el campo obligatorio: {field}"}), 400
            
        # Validacion tipos de datos correctos
        if not isinstance(data['postId'], str):
            return jsonify({"msg": "El campo postId debe ser tipo String"}), 400
        if not isinstance(data['description'], str):
            return jsonify({"msg": "El campo description debe ser tipo String"}), 400
        if not isinstance(data['size'], str):
            return jsonify({"msg": "El campo size debe ser tipo String"}), 400
        if not isinstance(data['fragile'], bool):
            return jsonify({"msg": "El campo fragile debe ser tipo Boolean"}), 400
        if not isinstance(data['offer'], int):
            return jsonify({"msg": "El campo offer debe ser tipo Integer"}), 400
        
        #Validacion de tamaño paquete correcto/oferta valorpositiva
        if data['size'] not in ['LARGE', 'MEDIUM', 'SMALL']:
            return jsonify({"msg": "El campo size debe ser una opcion entre: LARGE, MEDIUM, SMALL"}), 412
        if data['offer'] <= 0:
            return jsonify({"msg": "El campo offer debe ser un número entero positivo"}), 412
        nueva_oferta = Oferta(   
            userId =user_id,
            postId=post_id,
            description=description,
            size=size,
            fragile=fragile,
            offer=offer         
            
        )
        
        db.session.add(nueva_oferta)
        db.session.commit()       
        response_data = {

        "postId": nueva_oferta.postId,
        "id": nueva_oferta.id,
        "description": nueva_oferta.description,
        "size": nueva_oferta.size,
        "fragile" : nueva_oferta.fragile,
        "offer": nueva_oferta.offer,
        "userId":user_id,
        "createdAt":nueva_oferta.createdAt                      

        }

        print(response_data)
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"msg": "Error al crear el oferta", "error": str(e)}), 500
 

#Eliminar Oferta    
@oferta_bp.route('<string:id_oferta>', methods=['DELETE'])

def eliminar_Oferta(id_oferta):   
    authorization_header = request.headers.get('Authorization')
    user_id=""
    if authorization_header:
        token_valido = validarToken(authorization_header, True)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
        else:
            user_id=token_valido["id"]
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    
    try:
        # Id formato uuid      
        if not uuid.UUID(id_oferta):
                return None
        oferta=Oferta.query.get(id_oferta)
        #id existente
        if oferta is None:
            return jsonify({"msg": "La oferta con ese id no existe"}), 404  
        db.session.delete(oferta)
        db.session.commit()     
    except Exception as e:
        return jsonify({"msg": "El id no es un valor string con formato uuid"}), 400

    return jsonify({"msg": "la oferta fue eliminada"}), 200                    

#Reestablecer base de datos
@oferta_bp.route('/reset', methods=['POST'])
def reestablecer_basededatos():
    try:       
        Oferta.query.delete()
        db.session.commit()

        return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#Ping
@oferta_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"msg": "Pong"}), 200 



