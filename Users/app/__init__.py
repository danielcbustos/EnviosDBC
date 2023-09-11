from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from tests.test_config import TestConfig
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.url_map.strict_slashes = False
    if app.config.get("ENV") == "production":
        app.config.from_object(Config)
    else:
        app.config.from_object(TestConfig)

    db.init_app(app)

    from app.routes.usuario_Routes import usuario_bp
    app.register_blueprint(usuario_bp)
    return app
