from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from main import app, db
from main.commons.decorators import validate_request
from main.commons.exceptions import BadRequest, Unauthorized
from main.commons.utils import check_password, hash_password
from main.libs.jwt import generate_jwt_token
from main.models.user import UserModel
from main.schemas.user import PlainUserSchema, UserSignupSchema


@app.post("/users/signup")
@validate_request(body_schema=UserSignupSchema)
def signup(request_body):
    hashed_password = hash_password(request_body["password"])
    user = UserModel(email=request_body["email"], hashed_password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        raise BadRequest(error_message="Email already existed")
    access_token = create_access_token(identity=user.id, fresh=True)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}


@app.post("/users/login")
@validate_request(body_schema=PlainUserSchema)
def login(request_body):
    user: UserModel = UserModel.query.filter(
        UserModel.email == request_body["email"]
    ).one_or_none()

    if not user or not check_password(request_body["password"], user.hashed_password):
        raise Unauthorized(error_message="Email or password is incorrect")

    access_token = generate_jwt_token(user.id)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}
