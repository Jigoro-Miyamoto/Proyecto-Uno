from flask import Flask
from config import Config
from database_juegos import db
from routes_juegos.Juegos_routes import VideoJueos_bp

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(VideoJueos_bp, url_prefix = '/api')

with app.app_contex():
    db.create.all()
    
if __name__ == '__main__':
    app.run(debug = True)