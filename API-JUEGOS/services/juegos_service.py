from database.models import VideoJuego
from database import db

def get_video_juegos():
    return VideoJuego.query.all()

def get_video_juego(id):
    juego = VideoJuego.query.get(id)
    if not juego:
        return None
    return juego

def añadir_juego(data):
    nuevo = VideoJuego(titulo = data["titulo"],
                       genero = data["genero"],
                       horas_jugadas = data["horas_jugadas"])
    db.session.add(nuevo)
    db.session.commit()
    return nuevo

def patch_juego(id, data):
    juego = get_video_juego(id)
    if not juego:
        return None
    campos = ["titulo", "genero", "horas_jugadas"]
    for campo in campos:
        if campo in data:
            setattr(juego,campo, data[campo])
    db.session.commit()
    return juego

def delete_juego(id):
    juego = get_video_juego(id)
    if not juego:
        return False
    db.session.delete(juego)
    db.session.commit()
    return True



