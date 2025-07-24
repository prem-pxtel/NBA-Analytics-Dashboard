import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required

from db import get_db_connection
from utils import admin_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    pwd = data.get("password")
    invite_code = data.get("invite_code")

    if not username or not pwd:
        return jsonify({"error": "Missing username or password"}), 400
    pwd_hash = current_app.bcrypt.generate_password_hash(pwd).decode('utf-8')

    if invite_code == os.getenv("ADMIN_INVITE_CODE"):
        role = "admin"
    else:
        role = "viewer"

    print(os.getenv("ADMIN_INVITE_CODE"))
    print(invite_code)
    
    query = """
        INSERT INTO Users (username, pwd_hash, user_role)
        VALUES (%s, %s, %s); 
    """

    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute(query, (username, pwd_hash, role))
        db.commit()
        return jsonify({"message": "User registered successfully", "role":role}), 201
    except Exception as e:
        db.rollback()
        print("error occured on register", e)
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    pwd_raw = data.get("password")

    if not username or not pwd_raw:
        return jsonify({"error": "Missing username or password"}), 400
    
    query = """
        SELECT user_id, pwd_hash
        FROM Users
        WHERE username = %s;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (username,))
    user = cur.fetchone()
    db.close()

    if user:
        user_id, pwd_hash = user
        if current_app.bcrypt.check_password_hash(pwd_hash, pwd_raw):
            access_token = create_access_token(identity=str(user_id))
            print("--- Login successful ---")
            print(jsonify(access_token=access_token))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Wrong password"}), 401
    return jsonify({"error": "No such user found"}), 401

# for debugging
@auth_bp.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    from flask_jwt_extended import get_jwt_identity, get_jwt
    return jsonify({
        "user_id": get_jwt_identity(),
        "role": get_jwt().get("role")
    })


@auth_bp.route("/view_users", methods=["GET"])
@admin_required
def get_all_users():
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT user_id, username, user_role FROM Users")
    rows = cur.fetchall()
    db.close()

    users = [{"user_id": row[0], "username": row[1], "role": row[2]} for row in rows]
    return jsonify(users)
