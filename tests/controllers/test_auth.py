from datetime import timedelta
from time import sleep

from flask_jwt_extended import create_access_token

from main import app
from tests.utils.init_data import generate_auth_headers, init_users


def test_wrong_secret_key(client):
    user = init_users(number_of_user=1)[0]
    headers = generate_auth_headers(user_id=user.id)
    app.config.update(JWT_SECRET_KEY="other_secret_key")
    response = client.get("/categories", headers=headers)
    assert response.status_code == 401


def test_missing_header(client):
    response = client.get("/categories")
    assert response.status_code == 401


def test_missing_bearer(client):
    user = init_users(number_of_user=1)[0]
    token = create_access_token(identity=user.id, fresh=True)
    headers = {"Authorization": f"{token}"}
    response = client.get("/categories", headers=headers)
    assert response.status_code == 401


def test_expired_token(client):
    user = init_users(number_of_user=1)[0]
    app.config.update(JWT_ACCESS_TOKEN_EXPIRES=timedelta(seconds=2))
    headers = generate_auth_headers(user_id=user.id)
    response = client.get("/categories", headers=headers)
    assert response.status_code == 200
    sleep(2)
    response = client.get("/categories", headers=headers)
    assert response.status_code == 401
