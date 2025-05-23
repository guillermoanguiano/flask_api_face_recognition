from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registrar blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.client_routes import client_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(client_bp, url_prefix="/api")

    return app
