import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt
from flask_bcrypt import Bcrypt
from db import get_db_connection
from routes.auth import auth_bp
from routes.player_stats import player_stats_bp


def create_app(): 
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        with app.app_context():
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT role FROM User WHERE user_id = %s", (identity,))
            role = cur.fetchone()[0]
            print(role) # TODO: remove
            db.close()
            return {"role": role}

    def admin_required(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == "admin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"error": "You don't have permission"}), 403
        return decorator

    app.register_blueprint(auth_bp)
    app.register_blueprint(player_stats_bp)
    app.admin_required = admin_required

    return app

