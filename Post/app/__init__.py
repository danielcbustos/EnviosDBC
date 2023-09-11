from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from tests.test_config import TestConfig

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    if app.config.get("ENV") == "production":
        app.config.from_object(Config)
    else:
        app.config.from_object(TestConfig)
    db.init_app(app)

    from app.posts.publicacion_Posts import publicacion_bp
    app.register_blueprint(publicacion_bp)
    return app