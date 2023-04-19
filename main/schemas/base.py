from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()


class TrimmedStr(fields.Str):
    """String field which strips whitespace at the ends of the string."""

    def _deserialize(self, value, attr, data, **kwargs):
        """Deserialize string value."""
        value = super()._deserialize(value, attr, data, **kwargs)
        return value.strip()
