from flask_jwt_extended import create_access_token

from tests.utils.init_data import init_user


def test_missing_header(client):
    response = client.get("/categories")
    assert response.status_code == 401


def test_missing_bearer(client):
    user = init_user(number_of_user=1)[0]
    token = create_access_token(identity=user.id, fresh=True)
    headers = {"Authorization": f"{token}"}
    response = client.get("/categories", headers=headers)
    assert response.status_code == 401
