from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import validate_body
from main.commons.exceptions import BadRequest, Forbidden
from main.commons.utils import get_pagination_params
from main.models.category import CategoryModel
from main.schemas.category import CreateCategorySchema, PlainCategorySchema


@app.post("/categories")
@jwt_required()
@validate_body(CreateCategorySchema)
def create_category():
    request_data = request.get_json()
    current_user_id = get_jwt_identity()
    category = CategoryModel(**request_data, user_id=current_user_id)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Category name already existed")
    return PlainCategorySchema().dump(category)


@app.get("/categories")
@jwt_required()
def get_list_categories():
    offset, limit = get_pagination_params(request_args=request.args)
    categories = (
        CategoryModel.query.limit(limit)
        .offset(offset)
        .with_entities(
            CategoryModel.id,
            CategoryModel.name,
            CategoryModel.user_id,
            # CategoryModel.created_at,
            # CategoryModel.updated_at,
        )
        .all()
    )
    total = CategoryModel.query.count()
    return {
        "categories": [PlainCategorySchema().dump(category) for category in categories],
        "pagination": {"offset": offset, "limit": limit, "total": total},
    }


@app.get("/categories/<string:category_id>")
@jwt_required()
def get_detail_category(category_id):
    category = CategoryModel.query.get_or_404(int(category_id))
    return PlainCategorySchema().dump(category)


@app.delete("/categories/<string:category_id>")
@jwt_required()
def delete_category(category_id):
    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != get_jwt_identity():
        raise Forbidden(error_message="User has no right to delete this category")
    db.session.delete(category)
    db.session.commit()
    return ""