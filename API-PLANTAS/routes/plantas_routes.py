from flask import Blueprint, request, jsonify
import services.plantas_services as ps

plantas_bp = Blueprint("plantas_api", __name__)


@plantas_bp.route("/plantas", methods = ["POST"])

def post_planta_r():
    data = request.get_json()
    nueva_planta = ps.crear_planta(data)
    if not nueva_planta:
        return jsonify({"message": "Error al ingresar nueva planta"})
    return jsonify(nueva_planta.to_dict()), 201
@plantas_bp.route("/plantas", methods = ["GET"])

def get_plantas_r():
    plantas = ps.get_plantas()
    return jsonify(plantas),200

@plantas_bp.route("/plantas/<int:id>", methods = ["GET"])

def get_planta_r(id):
    planta = ps.get_planta(id)
    if not planta:
        return jsonify({"message":f"No se encontro la planta de id {id}"}), 404
    return jsonify(planta.to_dict()),200

@plantas_bp.route("/plantas/<int:id>", methods = ["PATCH"])

def patch_planta_r(id):
    data = request.get_json()
    if not data:
        return jsonify({"message":"Error, ingrese datos para actualizar"})
    planta = ps.patch_planta(id,data)
    if not planta:
        return jsonify({"message":f"No se encontro la planta de id {id}"}), 404
    return jsonify(planta.to_dict()),200
    

@plantas_bp.route("/plantas/<int:id>", methods = ["DELETE"])
def delete_planta_r(id):
    planta = ps.delete_planta(id)
    if not planta:
        return jsonify({"message":f"No se encontro la planta de id {id}"}), 404
    return jsonify({"message": "La planta se ha eliminado exitosamente"}), 204
    


    