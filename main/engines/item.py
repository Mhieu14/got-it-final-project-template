from sqlalchemy.exc import IntegrityError

from main import db
from main.commons.exceptions import BadRequest, NotFound
from main.models.item import ItemModel
from main.schemas.item import PlainItemSchema


def create_item(user_id, category_id, request_body):
    item = ItemModel(**request_body, user_id=user_id, category_id=category_id)
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
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
    if item is None:
        raise NotFound(error_message="Item not found")
    return item


def delete_item(item):
    db.session.delete(item)
    db.session.commit()


def update_item(item):
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return PlainItemSchema().dump(item)
