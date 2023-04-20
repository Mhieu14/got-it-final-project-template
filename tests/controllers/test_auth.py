from datetime import datetime, timedelta

import jwt

from main import config
from tests.utils.init_data import create_user


def test_wrong_secret_key(client):
    user = create_user()
    token = jwt.encode(
        payload={
            "sub": user.id,
            "exp": datetime.utcnow() + config.JWT_ACCESS_TOKEN_EXPIRES,
        },
        key="other_secret_key",
    )
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401


def test_missing_header(client):
    response = client.post("/categories")
    assert response.status_code == 401


def test_missing_bearer(client):
    user = create_user()
    token = jwt.encode(
        payload={
            "sub": user.id,
            "exp": datetime.utcnow() + config.JWT_ACCESS_TOKEN_EXPIRES,
        },
        key=config.JWT_SECRET_KEY,
    )
    headers = {"Authorization": token}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401


def test_invalid_token(client):
    headers = {"Authorization": "xxx.yyy.zzz"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401

    headers = {"Authorization": "Bearer xxx.yyy.zz"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401

    headers = {"Authorization": "Bearer xxx.yyy.zzz 12123"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401


def test_token_expired(client):
    user = create_user()
    token = jwt.encode(
        payload={
            "sub": user.id,
            "exp": datetime.utcnow() - timedelta(seconds=1),
        },
        key=config.JWT_SECRET_KEY,
    )
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/categories", headers=headers)
    assert response.status_code == 401
