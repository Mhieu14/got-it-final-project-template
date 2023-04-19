import main.engines.category as engine
from main import app
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import Forbidden
from main.schemas.category import PlainCategorySchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories")
@token_required
@validate_request(body_schema=PlainCategorySchema)
def create_category(user_id, request_body):
    category = engine.create_category(user_id, request_body)
    return PlainCategorySchema().dump(category)


@app.get("/categories")
@validate_request(query_schema=PaginationQuerySchema)
def get_categories(request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
    categories = engine.get_categories(offset, limit)
    total = engine.count_categories()
    return {
        "categories": PlainCategorySchema(many=True).dump(categories),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<int:category_id>")
def get_category(category_id):
    category = engine.get_category(category_id)
    return PlainCategorySchema().dump(category)


@app.delete("/categories/<int:category_id>")
@token_required
def delete_category(user_id, category_id):
    category = engine.get_category(category_id)
    if category.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this category")
    engine.delete_category(category)
    return {}
