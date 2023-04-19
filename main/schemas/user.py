from marshmallow import fields, validate

from main.constants import EMAIL_MAX_LENGTH, PASSWORD_MIN_LENGTH

from .base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(
        required=True,
        validate=validate.Length(max=EMAIL_MAX_LENGTH),
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(min=PASSWORD_MIN_LENGTH),
            validate.Regexp(
                # (?=.*[a-z]) - at least one lower case letter exists
                # (?=.*[A-Z]) - at least one upper case letter exists
                # (?=.*\d) - at least one digit exists
                regex=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])",
                error=(
                    "Passwords must include at least one lowercase letter, "
                    "one uppercase letter, one digit"
                ),
            ),
        ],
    )
