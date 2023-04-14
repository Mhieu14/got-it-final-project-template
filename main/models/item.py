from main import db

from .base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = "items"

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(5000))
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
