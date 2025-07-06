from flask import Blueprint, request, jsonify
from services_juegos import juegos_service as JS


VideoJuegos_bp = Blueprint('juegos_api', __name__)

@VideoJuegos_bp.route("/videojuegos", methods = ["POST"])
def añadir_juego_route():
    data = request.get_json()
    if not data:
        return jsonify({"message":"Ingresa todos los datos para continuar"})
    nuevo = JS.añadir_juego(data)
    return jsonify(nuevo.to_dict()), 201

@VideoJuegos_bp.route("/vodepjuegos", methods = ["GET"])

def get_juegos_route():
    juegos = JS.get_video_juegos
    return jsonify([juego.to_dict() for juego in juegos])

@VideoJuegos_bp.route("/videojuegos/<int:id>", methods = ["GET"])

def get_juego_route(id):
    juego = JS.get_video_juego(id)
    if not juego:
        return jsonify({"message":f"No se encontro el juego de id {id}"}), 404
    return jsonify(juego.to_dict())

@VideoJuegos_bp("/videojuesgos/<int:id>", methods = ["PATCH"])

def patch_juegos_route(id):
    data = request.get_json()
    if not data:
        return jsonify({"message":"Error, ingrese datos para actualizar"})
    juego = JS.patch_juego(id, data)
    if not juego:
        return jsonify({"message":f"No se encontro el juego de id {id}"}), 404
    return jsonify(juego.to_dict())

@VideoJuegos_bp("/videojuegos/<int:id>", methods = ["DELETE"])

def delete_juego_route(id):
    juego = JS.delete_juego(id)
    if not juego:
        return jsonify({"message":f"No se encontro el juego de id {id}"}), 404
    else:
        return jsonify({"message": "El juego se ha borrado exitosamente"}), 024

    

    
