from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest


def validate_body(schema):
    def validate(func):
        def wrapper(*args, **kwargs):
            request_data = request.get_json()
            try:
                schema().load(request_data)
            except ValidationError as err:
                # return BadRequest(error_message=err.messages).to_response()
                raise BadRequest(error_message=err.messages)
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return validate
