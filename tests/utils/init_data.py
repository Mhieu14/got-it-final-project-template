import main.engines.user as user_engine
from main import db
from main.libs.jwt import generate_jwt_token
from main.models.category import CategoryModel
from main.models.item import ItemModel


def create_users(number_of_users):
    users = []
    for i in range(number_of_users):
        user = user_engine.create_user(
            {"email": f"email{i}@email.com", "password": "passwordA1"}
        )
        users.append(user)
    db.session.commit()
    return users


def create_user():
    return create_users(number_of_users=1)[0]


def generate_auth_headers(user_id):
    token = generate_jwt_token(user_id)
    return {"Authorization": f"Bearer {token}"}


def create_categories(user_id, number_of_categories):
    categories = []
    for i in range(number_of_categories):
        cate = CategoryModel(
            name=f"cate{i}",
            description="Description",
            user_id=user_id,
        )
        db.session.add(cate)
        categories.append(cate)
    db.session.commit()
    return categories


def create_category(user_id):
    return create_categories(user_id=user_id, number_of_categories=1)[0]


def create_items(user_id, category_id, number_of_items):
    items = []
    for i in range(number_of_items):
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


def create_item(user_id, category_id):
    return create_items(user_id=user_id, category_id=category_id, number_of_items=1)[0]


def count_items_in_category(category_id):
    return ItemModel.query.filter(ItemModel.category_id == category_id).count()
