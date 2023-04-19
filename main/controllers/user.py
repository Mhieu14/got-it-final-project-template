from sqlalchemy.exc import IntegrityError

from main import app
from main.commons.decorators import validate_request
from main.commons.exceptions import BadRequest, Unauthorized
from main.commons.utils import check_password
from main.engines.user import create_user, get_user_by_email
from main.libs.jwt import generate_jwt_token
from main.schemas.user import UserSchema


@app.post("/users/signup")
@validate_request(body_schema=UserSchema)
def signup(request_body):
    try:
        user = create_user(
            email=request_body["email"], password=request_body["password"]
        )
    except IntegrityError:
        raise BadRequest(error_message="Email already existed")
    access_token = generate_jwt_token(user.id)
    return {"token": access_token, "user": UserSchema().dump(user)}


@app.post("/users/login")
@validate_request(body_schema=UserSchema)
def login(request_body):
    user = get_user_by_email(request_body["email"])
    if not user:
        raise Unauthorized(error_message="Email not existed")
    if not user or not check_password(request_body["password"], user.hashed_password):
        raise Unauthorized(error_message="Email or password is incorrect")
    access_token = generate_jwt_token(user.id)
    return {"token": access_token, "user": UserSchema().dump(user)}
