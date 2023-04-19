from sqlalchemy.exc import IntegrityError

import main.engines.item as engine
from main import app
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.engines.category import get_category
from main.schemas.item import ItemSchema, UpdateItemSchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories/<int:category_id>/items")
@token_required
@validate_request(body_schema=ItemSchema)
def create_item(user_id, category_id, request_body):
    category = get_category(category_id)
    if not category:
        raise NotFound(error_message="Category not found")
    try:
        item = engine.create_item(
            user_id=user_id,
            category_id=category_id,
            name=request_body["name"],
            description=request_body["description"],
        )
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return ItemSchema().dump(item)


@app.get("/categories/<int:category_id>/items")
@validate_request(query_schema=PaginationQuerySchema)
def get_items(category_id, request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
    category = get_category(category_id)
    if not category:
        raise NotFound(error_message="Category not found")
    items = engine.get_items(category_id, offset, limit)
    total = engine.count_items(category_id)
    return {
        "items": ItemSchema(many=True).dump(items),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def api_get_item(category_id, item_id):
    item = engine.get_item(category_id, item_id)
    if item is None:
        raise NotFound(error_message="Item not found")
    return ItemSchema().dump(item)


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@token_required
def api_delete_item(user_id, category_id, item_id):
    item = engine.get_item(category_id, item_id)
    if item is None:
        raise NotFound(error_message="Item not found")
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    engine.delete_item(item)
    return {}


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@token_required
@validate_request(body_schema=UpdateItemSchema)
def api_update_item(user_id, category_id, item_id, request_body):
    item = engine.get_item(category_id, item_id)
    if item is None:
        raise NotFound(error_message="Item not found")
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    if "name" in request_body:
        item.name = request_body["name"]
    if "description" in request_body:
        item.description = request_body["description"]
    try:
        engine.update_item(item)
    except IntegrityError:
        raise BadRequest(error_message="Item name already existed")
    return ItemSchema().dump(item)
