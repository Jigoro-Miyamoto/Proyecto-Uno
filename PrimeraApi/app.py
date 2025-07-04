# Importamos flask para crear nuestra api
## Especificamente, jsonify, Flask y request
from flask import Flask, jsonify, request 
'''
#?jsonify: Nos permite pasar un diccionario a un json
#? FLask
#? request: Especificar el tipo de solicitud de HTTP
'''
#! Podemos de igual manera crear una base de datos en el codigo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Crear DB
## configuracion de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///videojuegos.db"

# Inicializar la base de datos
db = SQLAlchemy(app)

# Definir el modelo de datos(Estructura de la tabla)
class VideoJuego(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50))
    genero = db.Column(db.String(50))
    horas_jugadas = db.Column(db.Integer)
    # Esta funcion solo hace mas sencillo comvertir los datos a un JSON
    def to_dict(self):
        return {
            "id" : self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "horas_jugadas": self.horas_jugadas,
        }
# Asegurra que las tablas de la base existan a la hora de inicializar
with app.app_context():
    db.create_all()

'''
@app.route va a definir la ruta de la api, en este caso, la URL y los métodos HTTP para cada
funcion.

'''
#! METODOS GET
@app.route('/videojuegos', methods = ['GET'])
def get_Video_Juegos():
    videojuegos = VideoJuego.query.all()

    return jsonify([VideoJuego.to_dict() for VideoJuego in videojuegos])
@app.route('/videojuegos/<int:id>', methods = ['GET'])
def get_Video_Juego(id):
    videoJuego = VideoJuego.query.get(id)
    if videoJuego:
        return jsonify(videoJuego.to_dict()), 200
    else:
        return jsonify({"error": "Juego no encontrado"}), 404

#! METODO POST
@app.route("/videojuegos", methods = ['POST'])
def crear_juego():
    datos = request.get_json() # Parsea la informacion

    nuevo_juego = VideoJuego(titulo = datos["titulo"],
                             genero = datos["genero"],
                             horas_jugadas = datos["horas_jugadas"])
    db.session.add(nuevo_juego)
    db.session.commit()

    return jsonify(nuevo_juego.to_dict()), 201

#! METODO PATCH
@app.route("/videojuegos/<int:id>", methods = ["PATCH"])
def set_juego(id):
    videoJuego = VideoJuego.query.get(id)
    data = request.get_json()
    if 'titulo' in data:
        videoJuego.titulo = data["titulo"]
    if 'genero' in data:
        videoJuego.genero = data["genero"]
    if 'horas_jugadas' in data:
        videoJuego.horas_jugadas = data["horas_jugadas"]
    
    # Esta linea basicamente guarda los datos
    db.session.commit()

    return jsonify(videoJuego.to_dict())

#! METODO DELTE
@app.route("/videojuegos/<int:id>", methods = ["DELETE"])

def delete_juego(id):
    videoJuego = VideoJuego.query.get(id)
    db.session.delete(videoJuego)
    db.session.commit()

    return jsonify({"message" : "Se eliminó el juego correctamente"}), 201


if __name__ == '__main__':
    app.run(debug = True)