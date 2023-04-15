from flask_jwt_extended import create_access_token

from main import db
from main.commons.utils import hash_password
from main.models.category import CategoryModel
from main.models.user import UserModel


def get_email_by_index(email_index):
    return f"email{email_index}@email.com"


def get_cate_name_by_index(cate_index, email_index):
    return f"cate{cate_index}_user{email_index}"


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


def generate_auth_headers(user_id):
    token = create_access_token(identity=user_id, fresh=True)
    return {"Authorization": f"Bearer {token}"}


def init_category(user_id, number_of_cate=10):
    cates = []
    for i in range(number_of_cate):
        cate = CategoryModel(
            name=get_cate_name_by_index(i, user_id),
            description="Description",
            user_id=user_id,
        )
        db.session.add(cate)
        cates.append(cate)
    db.session.commit()
    return cates
