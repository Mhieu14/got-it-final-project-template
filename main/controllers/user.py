from main import app
from main.commons.decorators import validate_request
from main.commons.exceptions import Unauthorized
from main.commons.utils import check_password
from main.engines.user import create_user, get_user_by_email
from main.libs.jwt import generate_jwt_token
from main.schemas.user import PlainUserSchema, UserSignupSchema


@app.post("/users/signup")
@validate_request(body_schema=UserSignupSchema)
def signup(request_body):
    user = create_user(request_body)
    access_token = generate_jwt_token(user.id)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}


@app.post("/users/login")
@validate_request(body_schema=PlainUserSchema)
def login(request_body):
    user = get_user_by_email(request_body["email"])

    if not user or not check_password(request_body["password"], user.hashed_password):
        raise Unauthorized(error_message="Email or password is incorrect")

    access_token = generate_jwt_token(user.id)
    return {"token": access_token, "user": PlainUserSchema().dump(user)}
