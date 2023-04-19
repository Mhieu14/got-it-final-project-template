from main import db
from main.commons.utils import hash_password
from main.models.user import UserModel


def create_user(email, password):
    hashed_password = hash_password(password)
    user = UserModel(email=email, hashed_password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    return UserModel.query.filter(UserModel.email == email).one_or_none()
