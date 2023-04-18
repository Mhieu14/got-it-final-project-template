from marshmallow import fields, post_load, validate

from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseSchema


class PlainCategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=NAME_MAX_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(max=DESCRIPTION_MAX_LENGTH)
    )

    @post_load
    def post_load_category(self, category, many, **kwargs):
        category["name"] = category["name"].strip()
        category["description"] = category["description"].strip()
        return category
