from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plantas.db"

db = SQLAlchemy(app)

class Planta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    especie = db.Column(db.String)
    nombre = db.Column(db.String(50))
    color = db.Column(db.String)
    forma_petalo = db.Column(db.String)
    indoor = db.Column(db.Boolean)
    flor = db.Column(db.Boolean)
    fr_riego_dias = db.Column(db.Integer)
    ultima_fecha_riego = db.Column(db.DateTime, nullable=True)
    notas = db.Column(db.Text)
    def to_dict(self):
        return {
            "id": self.id,
            "especie" : self.especie, 
            "nombre": self.nombre,
            "color":self.color,
            "forma_petalo":self.forma_petalo,
            "indoor":self.indoor,
            "flor":self.flor,
            "fr_riego_dias":self.fr_riego_dias,
            "ultima_fecha_riego":self.ultima_fecha_riego.isoformat()  if self.ultima_fecha_riego else None,
            "notas":self.notas
        }
    
with app.app_context():
    db.create_all()

@app.route("/plantas", methods = ["POST"])
def crear_planta():
    data = request.get_json()
    #Como se ocupa una fecha, SQLAlchemy espera un obj
    fecha_obj = None
    if "ultima_fecha_riego" in data and data["ultima_fecha_riego"] is not None:
        fechaIngresada = data["ultima_fecha_riego"]
        if not isinstance(fechaIngresada, str):
            return jsonify({"message" : "Formato de fecha invalido"})
        try:
            if 'T' in fechaIngresada and fechaIngresada is not None:
                fecha_obj = datetime.fromisoformat(fechaIngresada)
            else:                    
                fecha_obj = datetime.strptime(fechaIngresada, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": f"Formato de fecha invalido"})
        

    nueva_planta = Planta (nombre = data["nombre"],
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
    
    return jsonify(nueva_planta.to_dict()),201

@app.route("/plantas", methods = ["GET"])
def mostrar_plantas():
    plantas = Planta.query.all()
    return jsonify ([planta.to_dict() for planta in plantas])

@app.route("/plantas/<int:id>", methods = ["GET"])
def buscar_planta(id):
    planta = Planta.query.get(id)
    if planta:
        return jsonify(planta.to_dict()),202
    else:
        return jsonify({"message":"Planta no encontrada"}), 404

@app.route("/plantas/<int:id>", methods = ["PATCH"])
def actualizar_planta(id):
    planta = Planta.query.get(id)
    campos = ["nombre", "especie", "color", "forma_petalo", "indoor", "flor", 
              "fr_riego_dias", "ultima_fecha_riego", "notas"]
    if planta:
        data = request.get_json()
        for campo in campos:
            if campo in data:
                valor = data[campo]
                # Este es un manejo especial para las fechas
                if campo == ["ultima_fecha_riego"] and valor is not None:
                    try:
                        if 'T' in valor:
                            valor = datetime.fromisoformat(valor)
                        else:
                            valor = datetime.strptime(valor, "%Y-%m-%d")
                    except ValueError:
                        return jsonify({"message": f"Formato de fecha invalido para '{campo}'"})
                
                # Este es un manejo especial para los booleanos
                if campo in ["indoor", "flor"] and isinstance(valor, str):
                    if valor.lower() == 'true':
                        valor = True
                    if valor.lower() == 'false':
                        valor = False
                    else:
                        return jsonify({"message":f"Valor invalido para {campo}"})
                    
                setattr(planta, campo, valor)
        db.session.commit()
        return jsonify(planta.to_dict())
    else:
        return jsonify({"message":"Planta no encontrada"}), 404

@app.route("/plantas/<int:id>", methods = ["DELETE"])

def eliminar_planta(id):
    planta = Planta.query.get(id)
    if planta:
        db.session.delete(planta)
        db.session.commit()
        return jsonify({"message":"Planta eliminada"})
    else:
        return jsonify({"message":"Planta no encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
        