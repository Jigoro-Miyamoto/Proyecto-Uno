from flask import Flask
from config import Config
from database_juegos import db
from routes_juegos.Juegos_routes import VideoJuegos_bp

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(VideoJuegos_bp, url_prefix = '/api')

with app.app_context():

    db.create_all()
    
if __name__ == '__main__':
    app.run(debug = True)