import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes.auth import auth_bp
from routes.player_stats import player_stats_bp

def create_app(): 
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(player_stats_bp)

    return app
