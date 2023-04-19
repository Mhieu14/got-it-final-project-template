from flask_jwt_extended import create_access_token

from main import app
from tests.utils.init_data import create_users, generate_auth_headers


def test_wrong_secret_key(client):
    user = create_users(number_of_users=1)[0]
    headers = generate_auth_headers(user_id=user.id)
    app.config.update(JWT_SECRET_KEY="other_secret_key")
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401


def test_missing_header(client):
    response = client.post("/categories")
    assert response.status_code == 401


def test_missing_bearer(client):
    user = create_users(number_of_users=1)[0]
    token = create_access_token(identity=user.id, fresh=True)
    headers = {"Authorization": f"{token}"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401
