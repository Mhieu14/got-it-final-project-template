from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import validate_body
from main.commons.exceptions import BadRequest, Unauthorized
from main.commons.utils import check_password, hash_password
from main.models.user import UserModel
from main.schemas.user import PlainUserSchema, UserSignupSchema


@app.post("/users/signup")
@validate_body(UserSignupSchema)
def signup():
    request_data = request.get_json()
    hashed_password = hash_password(request_data["password"])
    user = UserModel(email=request_data["email"], hashed_password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Email already existed")
    access_token = create_access_token(identity=user.id, fresh=True)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}


@app.post("/users/login")
@validate_body(PlainUserSchema)
def login():
    request_data = request.get_json()
    user: UserModel = UserModel.query.filter(
        UserModel.email == request_data["email"]
    ).first()

    if not user or not check_password(request_data["password"], user.hashed_password):
        raise Unauthorized(error_message="Email or password is incorrect")

    access_token = create_access_token(identity=user.id, fresh=True)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}


# test auth
@app.get("/users/me")
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = UserModel.query.get_or_404(int(current_user_id))
    return PlainUserSchema().dump(user)
