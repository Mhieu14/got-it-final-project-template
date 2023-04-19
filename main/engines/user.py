from sqlalchemy.exc import IntegrityError

from main import db
from main.commons.exceptions import BadRequest, Unauthorized
from main.commons.utils import hash_password
from main.models.user import UserModel


def create_user(request_body):
    hashed_password = hash_password(request_body["password"])
    user = UserModel(email=request_body["email"], hashed_password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Email already existed")
    return user


def get_user_by_email(email):
    user: UserModel = UserModel.query.filter(UserModel.email == email).one_or_none()
    if not user:
        raise Unauthorized(error_message="Email not existed")
    return user
