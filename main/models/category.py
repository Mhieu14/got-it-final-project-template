from main import db
from main.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH

from .base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = db.Column(db.String(DESCRIPTION_MAX_LENGTH), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=False,
        nullable=False,
    )
