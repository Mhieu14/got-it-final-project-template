from marshmallow import ValidationError, fields, post_load, validates

from .base import BaseSchema


class PlainCategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    # created_at = fields.DateTime(dump_only=True)
    # updated_at = fields.DateTime(dump_only=True)

    @post_load
    def post_load_category(self, cate, many, **kwargs):
        cate["name"] = cate["name"].strip()
        cate["description"] = cate["description"].strip()
        return cate


class CreateCategorySchema(PlainCategorySchema):
    @validates("name")
    def validate_name(self, data, **kwargs):
        if len(data) > 255:
            raise ValidationError("Name must have less than 255 characters")

    @validates("description")
    def validate_description(self, data, **kwargs):
        if len(data) > 5000:
            raise ValidationError("Description must have less than 5000 characters")
