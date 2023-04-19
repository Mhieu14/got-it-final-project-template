import main.engines.item as engine
from main import app
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import Forbidden
from main.engines.category import get_category
from main.schemas.item import PlainItemSchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories/<int:category_id>/items")
@token_required
@validate_request(body_schema=PlainItemSchema)
def create_item(user_id, category_id, request_body):
    get_category(category_id)
    item = engine.create_item(user_id, category_id, request_body)
    return PlainItemSchema().dump(item)


@app.get("/categories/<int:category_id>/items")
@validate_request(query_schema=PaginationQuerySchema)
def get_items(category_id, request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
    get_category(category_id)
    items = engine.get_items(category_id, offset, limit)
    total = engine.count_items(category_id)
    return {
        "items": PlainItemSchema(many=True).dump(items),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def api_get_item(category_id, item_id):
    item = engine.get_item(category_id, item_id)
    return PlainItemSchema().dump(item)


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@token_required
def api_delete_item(user_id, category_id, item_id):
    item = engine.get_item(category_id, item_id)
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    engine.delete_item(item)
    return {}


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@token_required
@validate_request(body_schema=PlainItemSchema)
def api_update_item(user_id, category_id, item_id, request_body):
    item = engine.get_item(category_id, item_id)
    if item.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this item")
    item.name = request_body["name"]
    item.description = request_body["description"]
    engine.update_item(item)
    return PlainItemSchema().dump(item)
