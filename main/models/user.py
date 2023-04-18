from main import db
from main.constants import EMAIL_MAX_LENGTH, HASHED_PASSWORD_LENGTH

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    hashed_password = db.Column(db.String(HASHED_PASSWORD_LENGTH), nullable=False)
