from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import validate_body
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.commons.utils import get_pagination_params
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.item import PlainItemSchema


@app.post("/categories/<int:category_id>/items")
@jwt_required()
@validate_body(PlainItemSchema)
def create_item(category_id):
    request_data = request.get_json()
    current_user_id = get_jwt_identity()
    CategoryModel.query.get_or_404(category_id)
    item = ItemModel(**request_data, user_id=current_user_id, category_id=category_id)
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return PlainItemSchema().dump(item)


@app.get("/categories/<int:category_id>/items")
def get_items(category_id):
    offset, limit = get_pagination_params(request_args=request.args)
    CategoryModel.query.get_or_404(category_id)
    query = ItemModel.query.filter(ItemModel.category_id == category_id)
    items = (
        query.with_entities(
            ItemModel.id,
            ItemModel.name,
            ItemModel.user_id,
            ItemModel.category_id,
        )
        .limit(limit)
        .offset(offset)
    )
    total = query.count()
    return {
        "items": PlainItemSchema(many=True).dump(items),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


def get_one_item(category_id, item_id):
    item = (
        ItemModel.query.filter(ItemModel.id == item_id)
        .filter(ItemModel.category_id == category_id)
        .first()
    )
    if item is None:
        raise NotFound(error_message="Item not found")
    return item


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def get_item(category_id, item_id):
    item = get_one_item(category_id, item_id)
    return PlainItemSchema().dump(item)


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@jwt_required()
def delete_item(category_id, item_id):
    item = get_one_item(category_id, item_id)
    if item.user_id != get_jwt_identity():
        raise Forbidden(error_message="User has no right to delete this item")
    db.session.delete(item)
    db.session.commit()
    return {}


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@jwt_required()
@validate_body(PlainItemSchema)
def update_item(category_id, item_id):
    request_data = request.get_json()
    item = get_one_item(category_id, item_id)
    if item.user_id != get_jwt_identity():
        raise Forbidden(error_message="User has no right to delete this item")
    item.name = request_data["name"]
    item.description = request_data["description"]
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return PlainItemSchema().dump(item)
