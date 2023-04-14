from marshmallow import ValidationError, fields, post_load, validates

from .base import BaseSchema


class PlainItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def post_load_item(self, item, many, **kwargs):
        item["name"] = item["name"].strip()
        item["description"] = item["description"].strip()
        return item


class CreateItemSchema(PlainItemSchema):
    @validates("name")
    def validate_name(self, data, **kwargs):
        if len(data) > 255:
            raise ValidationError("Name must have less than 255 characters")

    @validates("description")
    def validate_description(self, data, **kwargs):
        if len(data) > 5000:
            raise ValidationError("Description must have less than 5000 characters")
