from main import db
from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = "items"

    name = db.Column(
        db.String(NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    description = db.Column(
        db.String(DESCRIPTION_MAX_LENGTH),
        nullable=False,
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=False,
        nullable=False,
    )
