from flask import request, jsonify, Blueprint
from app import db
from app.models.trayecto import Trayecto
from datetime import datetime
import uuid
from sqlalchemy import text
import requests
import os

trayecto_bp = Blueprint("trayecto", __name__, url_prefix="/routes")

def validarToken(token):
    parts = token.split()
    if len(parts) == 2 and parts[0] == 'Bearer':
        token1 = parts[1]

        url = f"{os.environ.get('USERS_PATH')}/users/me"
        headers = {'Authorization': f'Bearer {token1}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

@trayecto_bp.route('', methods=['GET'])
def obtener_Trayectos():
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
            
    flight_id = request.args.get('flight')

    if flight_id:
        if not isinstance(flight_id, str):
            return {}, 400
        trayectos = Trayecto.query.filter_by(flightId=flight_id).all()
    else:
        trayectos = Trayecto.query.all()

    trayectos_data = []
    for trayecto in trayectos:
        trayectos_data.append({
            "id": trayecto.id,
            "flightId": trayecto.flightId,
            "sourceAirportCode": trayecto.sourceAirportCode,
            "sourceCountry": trayecto.sourceCountry,
            "destinyAirportCode": trayecto.destinyAirportCode,
            "destinyCountry": trayecto.destinyCountry,
            "bagCost": trayecto.bagCost,
            "plannedStartDate": trayecto.plannedStartDate,
            "plannedEndDate": trayecto.plannedEndDate,
            "createdAt": trayecto.createdAt
        })

    return jsonify(trayectos_data), 200


@trayecto_bp.route('', methods=['POST'])
def crear_trayecto():
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    
    data = request.json
    required_fields = ["flightId", "sourceAirportCode", "sourceCountry", "destinyAirportCode",
                      "destinyCountry", "bagCost", "plannedStartDate", "plannedEndDate"]
    if not all(field in data for field in required_fields):
        return jsonify({}), 400

    flight_id = data.get('flightId')
    trayecto_existe = Trayecto.query.filter_by(flightId=flight_id).first()
    if trayecto_existe:
        return jsonify({}), 412
    source_airport_code = data.get('sourceAirportCode')
    source_country = data.get('sourceCountry')
    destiny_airport_code = data.get('destinyAirportCode')
    destiny_country = data.get('destinyCountry')
    bag_cost = data.get('bagCost')
    planned_start_date_iso = data.get('plannedStartDate')
    planned_end_date_iso = data.get('plannedEndDate')
    try:
        planned_start_date = datetime.fromisoformat(planned_start_date_iso[:-1] if planned_start_date_iso.endswith('Z') else planned_start_date_iso)
        planned_end_date = datetime.fromisoformat(planned_end_date_iso[:-1] if planned_end_date_iso.endswith('Z') else planned_end_date_iso)
        if planned_start_date > planned_end_date or planned_start_date < datetime.utcnow() or planned_end_date < datetime.utcnow():
            return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
    except Exception as e:
        return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
    try:
        nuevo_trayecto = Trayecto(
            flightId=flight_id,
            sourceAirportCode=source_airport_code,
            sourceCountry=source_country,
            destinyAirportCode=destiny_airport_code,
            destinyCountry=destiny_country,
            bagCost=bag_cost,
            plannedStartDate=planned_start_date,
            plannedEndDate=planned_end_date
        )
        
        db.session.add(nuevo_trayecto)
        db.session.commit()
        trayecto_creado= Trayecto.query.filter_by(flightId=nuevo_trayecto.flightId).first()
        return jsonify({"id": f"{trayecto_creado.id}", "createdAt" : f"{trayecto_creado.createdAt}"}), 201
    except Exception as e:
        return jsonify({"msg": "Error al crear el trayecto"}), 500
    

@trayecto_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({}), 200 

@trayecto_bp.route('/<string:id>', methods=['GET'])
def obtener_trayecto_por_id(id):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    try:
        id_to_find = uuid.UUID(id)
    except ValueError:
        return {}, 400
    query = text(f"SELECT * FROM trayecto WHERE id = '{id_to_find}'")
    trayecto = db.session.execute(query).fetchone()

    if trayecto is None:
        return jsonify({"msg": "El trayecto con ese id no existe"}), 404

    return jsonify({
        "id": trayecto.id,
        "flightId": trayecto.flightId,
        "sourceAirportCode": trayecto.sourceAirportCode,
        "sourceCountry": trayecto.sourceCountry,
        "destinyAirportCode": trayecto.destinyAirportCode,
        "destinyCountry": trayecto.destinyCountry,
        "bagCost": trayecto.bagCost,
        "plannedStartDate": trayecto.plannedStartDate,
        "plannedEndDate": trayecto.plannedEndDate,
        "createdAt": trayecto.createdAt
    }), 200

@trayecto_bp.route('/<string:id>', methods=['DELETE'])
def eliminar_trayecto_por_id(id):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token_valido = validarToken(authorization_header)
        if not(token_valido):
            return jsonify({"msg":"Token invalido"}), 401
    else:
        return jsonify({"msg":"Token no encontrado"}), 403
    try:
        id_to_find = uuid.UUID(id)
    except ValueError:
        return {}, 400
    consulta = db.session.execute(text(f"SELECT * FROM trayecto WHERE id = '{id_to_find}'"))
    trayecto_existe = consulta.fetchone()
    if trayecto_existe is None:
        return jsonify(), 404
    query = text(f"DELETE FROM trayecto WHERE id = '{id_to_find}'")
    
    try:
        db.session.execute(query)
        db.session.commit()
        return jsonify({ "msg": "el trayecto fue eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al eliminar el trayecto", "error": str(e)}), 500
    

@trayecto_bp.route('/reset', methods=['POST'])
def limpiar_tabla_trayectos():
    try:
        db.session.query(Trayecto).delete()
        db.session.commit()
        return jsonify({"msg": "Todos los datos fueron eliminados"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({}), 500
