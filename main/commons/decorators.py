from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, _ErrorCode


def validate_body(schema):
    def validate(func):
        def wrapper(*args, **kwargs):
            request_data = request.get_json()
            try:
                schema().load(request_data)
            except ValidationError as err:
                raise BadRequest(
                    error_message=err.messages, error_code=_ErrorCode.VALIDATION_ERROR
                )
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return validate
