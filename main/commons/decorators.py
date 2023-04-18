from functools import wraps

from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, _ErrorCode


def validate_body(schema):
    def validate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request_data = request.get_json()
                schema().load(request_data)
            except Exception as err:
                print(err)
                raise BadRequest(
                    error_message="Invalid request body",
                    error_data=err.messages
                    if isinstance(err, ValidationError)
                    else None,
                    error_code=_ErrorCode.VALIDATION_ERROR,
                )
            return func(*args, **kwargs)

        return wrapper

    return validate
