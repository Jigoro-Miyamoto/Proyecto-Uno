# Toda la logica de negocio iria en esta carpeta
## Nos va a permitir simplificar codigo y cumplir con ciertos requisitos


from database.models import Planta
from database import db
from datetime import datetime

# Primero: Definir auxiliares para metodos CRUD

def verificar_fecha(value):
    if value is None:
        return None
    if not isinstance(value, str):
     return None
    try:
        if 'T' in value:
            return datetime.fromisoformat(value)
        else:
            return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
            return None
     

def verificar_bool(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            return None
    else:
        return None
    
def check_requeridos(data):
    requeridos = ["especie", "nombre", "color", "indoor", "flor", "fr_riego_dias"]
    for requerido in requeridos:
        if data.get(requerido) is None:
            return False
    return True

def crear_planta(data):
    if not data:
        return None
    if not check_requeridos(data):
        return None
    fecha_obj = None
    if "ultima_fecha_riego" in data and data["ultima_fecha_riego"] is not None:
        fecha_obj = verificar_fecha(data["ultima_fecha_riego"])
    
    nueva_planta = Planta(nombre = data["nombre"],
                        especie = data["especie"],
                        color = data["color"],
                        forma_petalo = data["forma_petalo"],
                        indoor = data["indoor"],
                        flor = data["flor"],
                        fr_riego_dias = data["fr_riego_dias"],
                        ultima_fecha_riego = fecha_obj,
                        notas = data["notas"])
    db.session.add(nueva_planta)
    db.session.commit()
    return nueva_planta

def get_plantas():
    plantas = Planta.query.all()
    return [planta.to_dict() for planta in plantas]

def get_planta(id):
    planta = Planta.query.get(id)
    if not planta:
        return None
    return Planta

def patch_planta(id, data):
    if not data:
        return None
    planta = get_planta(id)
    if not planta:
        return None
    campos = ["nombre", "especie", "color", "forma_petalo", "indoor", "flor",
              "fr_riego_dias", "ultima_fecha_riego", "notas"]
    for campo in campos:
        if campo in data:
            valor = data[campo]
            if campo == "ultima_fecha_riego":
                valor = verificar_fecha(data["ultima_fecha_riego"])
            elif campo in ["indoor", "flor"]:
                valor = verificar_bool(valor)
            setattr(planta, campo, valor)
    db.session.commit()
    return planta

def delete_planta(id):
    planta = get_planta(id)
    if not planta:
        return False
    else:
        db.session.delete(planta)
        db.session.commit()
        return True
    
                
        
    