from flask_jwt_extended import create_access_token

from main import db
from main.commons.utils import hash_password
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def init_users(number_of_user=2):
    users = []
    for i in range(number_of_user):
        email = f"email{i}@email.com"
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
    categories = []
    for i in range(number_of_cate):
        cate = CategoryModel(
            name=f"cate{i}",
            description="Description",
            user_id=user_id,
        )
        db.session.add(cate)
        categories.append(cate)
    db.session.commit()
    return categories


def init_item(user_id, category_id, number_of_item=10):
    items = []
    for i in range(number_of_item):
        cate = ItemModel(
            name=f"item{i}",
            description="Description",
            category_id=category_id,
            user_id=user_id,
        )
        db.session.add(cate)
        items.append(cate)
    db.session.commit()
    return items


def count_items_in_category(category_id):
    return ItemModel.query.filter(ItemModel.category_id == category_id).count()
