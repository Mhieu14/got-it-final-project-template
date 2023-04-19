from main import db
from main.models.item import ItemModel
from main.schemas.item import ItemSchema


def create_item(user_id, category_id, name, description):
    item = ItemModel(
        name=name,
        description=description,
        user_id=user_id,
        category_id=category_id,
    )
    db.session.add(item)
    db.session.commit()
    return item


def get_items(category_id, offset, limit):
    items = (
        ItemModel.query.filter(ItemModel.category_id == category_id)
        .with_entities(
            ItemModel.id,
            ItemModel.name,
            ItemModel.user_id,
            ItemModel.category_id,
        )
        .limit(limit)
        .offset(offset)
    )
    return items


def count_items(category_id):
    return ItemModel.query.filter(ItemModel.category_id == category_id).count()


def get_item(category_id, item_id):
    item = (
        ItemModel.query.filter(ItemModel.id == item_id)
        .filter(ItemModel.category_id == category_id)
        .one_or_none()
    )
    return item


def delete_item(item):
    db.session.delete(item)
    db.session.commit()


def update_item(item):
    db.session.add(item)
    db.session.commit()
    return ItemSchema().dump(item)
