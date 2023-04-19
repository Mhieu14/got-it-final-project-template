from marshmallow import fields, validate

from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseSchema, TrimmedStr


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = TrimmedStr(
        required=True,
        validate=validate.Length(max=NAME_MAX_LENGTH),
    )
    description = TrimmedStr(
        required=True,
        validate=validate.Length(max=DESCRIPTION_MAX_LENGTH),
    )
