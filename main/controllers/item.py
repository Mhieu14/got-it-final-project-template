from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.item import PlainItemSchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories/<int:category_id>/items")
@token_required
@validate_request(body_schema=PlainItemSchema)
def create_item(user_id, category_id, request_body):
    CategoryModel.query.get_or_404(category_id)
    item = ItemModel(**request_body, user_id=user_id, category_id=category_id)
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return PlainItemSchema().dump(item)


@app.get("/categories/<int:category_id>/items")
@validate_request(query_schema=PaginationQuerySchema)
def get_items(category_id, request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
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
        .one_or_none()
    )
    if item is None:
        raise NotFound(error_message="Item not found")
    return item


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def get_item(category_id, item_id):
    item = get_one_item(category_id, item_id)
    return PlainItemSchema().dump(item)


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@token_required
def delete_item(user_id, category_id, item_id):
    item = get_one_item(category_id, item_id)
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    db.session.delete(item)
    db.session.commit()
    return {}


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@token_required
@validate_request(body_schema=PlainItemSchema)
def update_item(user_id, category_id, item_id, request_body):
    item = get_one_item(category_id, item_id)
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    item.name = request_body["name"]
    item.description = request_body["description"]
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return PlainItemSchema().dump(item)
