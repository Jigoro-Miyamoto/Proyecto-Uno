
from . import db

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