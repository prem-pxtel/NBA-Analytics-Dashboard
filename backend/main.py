import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask 
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from db import db_init, get_db_connection
from routes.auth import auth_bp
from routes.player_stats import player_stats_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        with app.app_context():
            db = get_db_connection()
            cur = db.cursor()
            cur.execute(
                "SELECT user_role FROM Users WHERE user_id = %s", (identity,))
            role = cur.fetchone()[0]
            db.close()
            return {"role": role}

    app.register_blueprint(auth_bp)
    app.register_blueprint(player_stats_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.bcrypt = Bcrypt(app)

    db_init()

    app.run(host=os.getenv("FLASK_RUN_HOST"),
            port=os.getenv("FLASK_RUN_PORT"), debug=True)
