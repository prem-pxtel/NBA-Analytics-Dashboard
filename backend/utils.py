from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") == "admin":
            return fn(*args, **kwargs)
        else:
            return jsonify({"error": "You don't have permission"}), 403
    return decorator
