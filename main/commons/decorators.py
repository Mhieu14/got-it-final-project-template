from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, _ErrorCode


def validate_body(schema):
    def validate(func):
        def wrapper(*args, **kwargs):
            try:
                request_data = request.get_json()
                schema().load(request_data)
            except ValidationError as err:
                raise BadRequest(
                    error_message=err.messages, error_code=_ErrorCode.VALIDATION_ERROR
                )
            except Exception:
                raise BadRequest(
                    error_message="Invalid request body",
                    error_code=_ErrorCode.VALIDATION_ERROR,
                )
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return validate
