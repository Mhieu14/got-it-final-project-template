from main import db
from main.models.category import CategoryModel


def create_category(user_id, name, description):
    category = CategoryModel(name=name, description=description, user_id=user_id)
    db.session.add(category)
    db.session.commit()
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
    return CategoryModel.query.get(category_id)


def delete_category(category):
    db.session.delete(category)
    db.session.commit()
