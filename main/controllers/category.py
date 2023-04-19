from sqlalchemy.exc import IntegrityError

import main.engines.category as engine
from main import app
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.schemas.category import CategorySchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories")
@token_required
@validate_request(body_schema=CategorySchema)
def create_category(user_id, request_body):
    try:
        category = engine.create_category(
            user_id=user_id,
            name=request_body["name"],
            description=request_body["description"],
        )
    except IntegrityError:
        raise BadRequest(error_message="Category name already existed")
    return CategorySchema().dump(category)


@app.get("/categories")
@validate_request(query_schema=PaginationQuerySchema)
def get_categories(request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
    categories = engine.get_categories(offset, limit)
    total = engine.count_categories()
    return {
        "categories": CategorySchema(many=True).dump(categories),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<int:category_id>")
def get_category(category_id):
    category = engine.get_category(category_id)
    if not category:
        raise NotFound(error_message="Category not found")
    return CategorySchema().dump(category)


@app.delete("/categories/<int:category_id>")
@token_required
def delete_category(user_id, category_id):
    category = engine.get_category(category_id)
    if not category:
        raise NotFound(error_message="Category not found")
    if category.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this category")
    engine.delete_category(category)
    return {}
