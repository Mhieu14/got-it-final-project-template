from main import db

from .base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(5000))
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
