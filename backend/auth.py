import hashlib
from flask import Blueprint, request, jsonify

auth_blueprint = Blueprint("auth", __name__)

def hash_pwd(pwd: str):
    return hashlib.sha256(pwd.encode()).hexdigest()

@auth_blueprint.route("/api/register", methods=["POST"])
def register_user():
    return

@auth_blueprint.route("/api/login", methods=["POST"])
def login():
    return