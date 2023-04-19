from marshmallow import fields, validate

from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseSchema, TrimmedStr


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(dump_only=True)
    name = TrimmedStr(
        required=True,
        validate=validate.Length(max=NAME_MAX_LENGTH),
    )
    description = TrimmedStr(
        required=True,
        validate=validate.Length(max=DESCRIPTION_MAX_LENGTH),
    )


class UpdateItemSchema(BaseSchema):
    name = TrimmedStr(
        validate=validate.Length(max=NAME_MAX_LENGTH),
    )
    description = TrimmedStr(
        validate=validate.Length(max=DESCRIPTION_MAX_LENGTH),
    )
