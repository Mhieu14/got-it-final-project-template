from functools import wraps

from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, Unauthorized, _ErrorCode
from main.libs.jwt import validate_jwt_token


def validate_request_body(body_schema):
    try:
        request_data = request.get_json()
        validated_data = body_schema().load(request_data)
    except ValidationError as err:
        raise BadRequest(
            error_message="Request body validation fail",
            error_data=err.messages,
            error_code=_ErrorCode.VALIDATION_ERROR,
        )
    except Exception:
        raise BadRequest(
            error_message="Invalid request body",
            error_code=_ErrorCode.VALIDATION_ERROR,
        )
    return validated_data


def validate_request_query(query_schema):
    try:
        request_query = request.args
        validated_query = query_schema().load(request_query)
    except ValidationError as err:
        raise BadRequest(
            error_message="Request query parameters validation fail",
            error_data=err.messages,
            error_code=_ErrorCode.VALIDATION_ERROR,
        )
    except Exception:
        raise BadRequest(
            error_message="Invalid request query parameters",
            error_code=_ErrorCode.VALIDATION_ERROR,
        )
    return validated_query


def validate_request(body_schema=None, query_schema=None):
    def validate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if body_schema:
                kwargs["request_body"] = validate_request_body(body_schema)
            if query_schema:
                kwargs["request_query"] = validate_request_query(query_schema)

            return func(*args, **kwargs)

        return wrapper

    return validate


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise Unauthorized(error_message="Missing Authorization Header")

        authorization_header = request.headers["Authorization"]
        if authorization_header.startswith("Bearer "):
            _, token = authorization_header.split(maxsplit=1)
            user_id = validate_jwt_token(token)
        else:
            raise Unauthorized(error_message="Invalid token type")

        kwargs["user_id"] = user_id
        return func(*args, **kwargs)

    return wrapper
