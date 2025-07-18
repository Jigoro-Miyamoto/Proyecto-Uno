from flask import Flask

from config_planta import Config
from  database import db
from routes.plantas_routes import plantas_bp
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(plantas_bp, url_prefix = '/api')


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
        