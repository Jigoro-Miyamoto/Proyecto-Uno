from . import db

class Planta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    especie = db.Column(db.String, nullable = False)
    nombre = db.Column(db.String(50), nullable = False)
    color = db.Column(db.String, nullable = False)
    forma_petalo = db.Column(db.String)
    indoor = db.Column(db.Boolean, nullable = False)
    flor = db.Column(db.Boolean)
    fr_riego_dias = db.Column(db.Integer, nullable = False)
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