import re

from marshmallow import ValidationError, fields, validate, validates

from main.constants import EMAIL_MAX_LENGTH, PASSWORD_MIN_LENGTH

from .base import BaseSchema

# (?=.*[a-z]) - at least one lower case letter exists
# (?=.*[A-Z]) - at least one upper case letter exists
# (?=.*\d) - at least one digit exists
password_pattern = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])")


class PlainUserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=EMAIL_MAX_LENGTH))
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=PASSWORD_MIN_LENGTH),
    )


class UserSignupSchema(PlainUserSchema):
    @validates("password")
    def validate_password(self, data, **__):
        if not password_pattern.match(data):
            raise ValidationError(
                "Passwords must include at least one lowercase letter, "
                "one uppercase letter, one digit"
            )
