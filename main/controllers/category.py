from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import token_required, validate_request
from main.commons.exceptions import BadRequest, Forbidden
from main.models.category import CategoryModel
from main.schemas.category import PlainCategorySchema
from main.schemas.pagination import PaginationQuerySchema


@app.post("/categories")
@token_required
@validate_request(body_schema=PlainCategorySchema)
def create_category(user_id, request_body):
    category = CategoryModel(**request_body, user_id=user_id)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Category name already existed")
    return PlainCategorySchema().dump(category)


@app.get("/categories")
@validate_request(query_schema=PaginationQuerySchema)
def get_categories(request_query):
    offset = request_query["offset"]
    limit = request_query["limit"]
    categories = (
        CategoryModel.query.limit(limit)
        .offset(offset)
        .with_entities(
            CategoryModel.id,
            CategoryModel.name,
            CategoryModel.user_id,
        )
        .all()
    )
    total = CategoryModel.query.count()
    return {
        "categories": PlainCategorySchema(many=True).dump(categories),
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<int:category_id>")
def get_category(category_id):
    category = CategoryModel.query.get_or_404(category_id)
    return PlainCategorySchema().dump(category)


@app.delete("/categories/<int:category_id>")
@token_required
def delete_category(user_id, category_id):
    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != user_id:
        raise Forbidden(error_message="User has no right to delete this category")
    db.session.delete(category)
    db.session.commit()
    return {}
