from datetime import datetime
from functools import wraps

import jwt
from flask import request

from main import app
from main.commons.exceptions import Unauthorized


def validate_jwt_token(token):
    try:
        data = jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms="HS256")
        return data["sub"]
    except Exception as err:
        raise Unauthorized(error_message=f"Invalid JWT token: {str(err)}")


def generate_jwt_token(user_id):
    return jwt.encode(
        payload={
            "sub": user_id,
            "exp": datetime.utcnow() + app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        },
        key=app.config["JWT_SECRET_KEY"],
    )


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise Unauthorized(error_message="Missing Authorization Header")

        authorization_header = request.headers["Authorization"]
        [token_type, token] = authorization_header.split()
        user_id = None

        if token_type == "Bearer":
            user_id = validate_jwt_token(token)
        if user_id is None:
            raise Unauthorized(error_message="Invalid token type")

        return func(user_id=user_id, *args, **kwargs)

    return wrapper
