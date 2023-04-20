from datetime import datetime

import jwt

from main import config


def validate_jwt_token(token):
    data = jwt.decode(token, config.JWT_SECRET_KEY, algorithms="HS256")
    return data["sub"]


def generate_jwt_token(subject):
    return jwt.encode(
        payload={
            "sub": subject,
            "exp": datetime.utcnow() + config.JWT_ACCESS_TOKEN_EXPIRES,
        },
        algorithm="HS256",
        key=config.JWT_SECRET_KEY,
    )
