from datetime import datetime

import jwt

from main import config
from main.commons.exceptions import Unauthorized


def validate_jwt_token(token):
    try:
        data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms="HS256")
        return data["sub"]
    except Exception as err:
        raise Unauthorized(error_message=f"Invalid JWT token: {err}")


def generate_jwt_token(subject):
    return jwt.encode(
        payload={
            "sub": subject,
            "exp": datetime.utcnow() + config.JWT_ACCESS_TOKEN_EXPIRES,
        },
        algorithm="HS256",
        key=config.JWT_SECRET_KEY,
    )
