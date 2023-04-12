from main import db

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
