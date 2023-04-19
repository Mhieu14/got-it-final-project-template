from sqlalchemy.exc import IntegrityError

from main import db
from main.commons.exceptions import BadRequest
from main.models.category import CategoryModel


def create_category(user_id, request_body):
    category = CategoryModel(**request_body, user_id=user_id)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Category name already existed")
    return category


def get_categories(offset, limit):
    categories = (
        CategoryModel.query.with_entities(
            CategoryModel.id,
            CategoryModel.name,
            CategoryModel.user_id,
        )
        .limit(limit)
        .offset(offset)
        .all()
    )
    return categories


def count_categories():
    return CategoryModel.query.count()


def get_category(category_id):
    return CategoryModel.query.get_or_404(category_id)


def delete_category(category):
    db.session.delete(category)
    db.session.commit()
