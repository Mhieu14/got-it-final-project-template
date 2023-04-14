from flask_jwt_extended import create_access_token

from main import db
from main.commons.utils import hash_password
from main.models.user import UserModel


def get_email_by_index(email_index):
    return f"email{email_index}@email.com"


def get_cate_name_by_index(cate_index, email_index):
    return f"cate{cate_index}_email{email_index}"


def init_user(number_of_user=2):
    users = []
    for i in range(number_of_user):
        email = get_email_by_index(i)
        password = "passwordA1"
        hashed_password = hash_password(password)
        user = UserModel(email=email, hashed_password=hashed_password)
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users


def generate_auth_headers(email_index=0):
    users = init_user(number_of_user=1)
    token = create_access_token(identity=users[0].id, fresh=True)
    return {"Authorization": f"Bearer {token}"}


def get_user_by_index(email_index=0):
    user: UserModel = UserModel.query.filter(
        UserModel.email == f"email{email_index}@email.com"
    ).first()
    return user


def init_category(email_index=0, number_of_cate=10):
    user = get_user_by_index(email_index)
    cates = []
    for i in range(number_of_cate):
        cate = UserModel(
            name=get_cate_name_by_index(i, email_index),
            description="Description",
            user_id=user.id,
        )
        db.session.add(cate)
        cates.append(cate)
    db.session.commit()
    return cates
