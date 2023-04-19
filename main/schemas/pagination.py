from marshmallow import fields, validate

from main.constants import LIMIT_DEFAULT, LIMIT_MAX, OFFSET_DEFAULT

from .base import BaseSchema


class PaginationQuerySchema(BaseSchema):
    offset = fields.Integer(
        load_default=OFFSET_DEFAULT,
        validate=validate.Range(min=0),
    )
    limit = fields.Integer(
        load_default=LIMIT_DEFAULT,
        validate=validate.Range(min=0, max=LIMIT_MAX),
    )
