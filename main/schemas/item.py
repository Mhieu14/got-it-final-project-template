from marshmallow import fields, post_load, validate

from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseSchema


class PlainItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=NAME_MAX_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(max=DESCRIPTION_MAX_LENGTH)
    )

    @post_load
    def post_load_item(self, item, many, **kwargs):
        item["name"] = item["name"].strip()
        item["description"] = item["description"].strip()
        return item
