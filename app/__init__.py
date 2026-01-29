from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Configuración básica
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "http://localhost:5173"}}
    )

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    # Registrar rutas
    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    from app.routes.spaces import spaces_bp
    app.register_blueprint(spaces_bp)

    from app.routes.reservations import reservations_bp
    app.register_blueprint(reservations_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app