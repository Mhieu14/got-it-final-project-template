import re

from marshmallow import ValidationError, fields, post_load, validates

from .base import BaseSchema


class PlainUserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def post_load_user(self, item, many, **kwargs):
        item["email"] = item["email"].lower().strip()
        return item


class UserSignupSchema(PlainUserSchema):
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
