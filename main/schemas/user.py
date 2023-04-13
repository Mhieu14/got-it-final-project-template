import re

from marshmallow import ValidationError, fields, validates

from .base import BaseSchema


class UserSignupSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates("email")
    def validate_email(self, data, **kwargs):
        if len(data) > 255:
            raise ValidationError("Email must have less than 255 characters")

    @validates("password")
    def validate_password(self, data, **kwargs):
        if len(data) < 6:
            raise ValidationError("Passwords must have at least 6 characters")

        # (?=.*[a-z]) - at least one lower case letter exists
        # (?=.*[A-Z]) - at least one upper case letter exists
        # (?=.*\d) - at least one digit exists
        pattern = re.compile("(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])")
        if not pattern.match(data):
            raise ValidationError(
                "Passwords must include at least one lowercase letter, "
                "one uppercase letter, one digit"
            )


class UserLoginSchema(BaseSchema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
