from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request, get_jwt
from db import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    pwd = data.get("password")
    role = data.get("role", "viewer")

    if not username or not pwd:
        return jsonify({"error": "Missing username or password"}), 400
    pwd_hash = current_app.bcrypt.generate_password_hash(pwd).decode('utf-8')
    add_user_query = f"""
        INSERT INTO User (username, password_hash, role) 
        VALUES ({username}, {pwd_hash}, {role}) 
    """

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute(add_user_query)
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    pwd_raw = data.get("password")

    if not username or not pwd_raw:
        return jsonify({"error": "Missing username or password"}), 400

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f"SELECT user_id, password_hash FROM User WHERE username = {username}'")
    user = cur.fetchone()
    db.close()

    if user:
        user_id, pwd_hash = user
        if current_app.bcrypt.check_password_hash(pwd_hash, pwd_raw):
            access_token = create_access_token(identity=user_id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Wrong password"}), 401
    return jsonify({"error": "No such user found"}), 401


def admin_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == "admin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"error": "You don't have permission"}), 403

        return decorator
    return wrapper

