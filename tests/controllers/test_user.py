import pytest

from main.commons.exceptions import BadRequest, ValidationError
from main.constants import EMAIL_MAX_LENGTH

default_email = "email0@email.com"
default_password = "passwordA1"


def test_signup_success(client):
    email = "email@email.com"
    password = "passwordA1"
    request_body = {"email": email, "password": password}
    response = client.post("/users/signup", json=request_body)
    assert response.status_code == 200
    assert "token" in response.json
    assert "user" in response.json
    assert "id" in response.json["user"]
    assert response.json["user"]["email"] == email


@pytest.mark.parametrize(
    "request_body",
    [
        None,
        {},
        {"email": default_email},
        {"password": default_password},
        {"email": "email", "password": default_password},
        {"email": default_email, "password": "invalid_password"},
        {
            "email": "a" * (EMAIL_MAX_LENGTH + 1) + "@email.com",
            "password": default_password,
        },
        {"email": default_email, "password": "shoR1"},
    ],
)
def test_signup_invalid_body(client, request_body):
    # missing password
    response = client.post("/users/signup", json=request_body)
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code


def test_signup_email_existed(client):
    request_body = {"email": default_email, "password": default_password}
    client.post("/users/signup", json=request_body)
    response = client.post("/users/signup", json=request_body)
    assert response.status_code == 400
    assert response.json["error_code"] == BadRequest.error_code


def test_login_success(client):
    request_body = {"email": default_email, "password": default_password}
    client.post("/users/signup", json=request_body)
    response = client.post("/users/login", json=request_body)
    assert response.status_code == 200
    assert "token" in response.json
    assert "user" in response.json
    assert "id" in response.json["user"]
    assert response.json["user"]["email"] == default_email


def test_login_fail(client):
    request_body = {"email": default_email, "password": default_password}
    client.post("/users/signup", json=request_body)

    # missing email
    response = client.post("/users/login", json={"password": default_password})
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code

    # missing password
    response = client.post("/users/login", json={"email": default_email})
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code

    # wrong email
    response = client.post(
        "/users/login", json={"email": "wrong@email.com", "password": default_password}
    )
    assert response.status_code == 401

    # wrong password
    response = client.post(
        "/users/login", json={"email": default_email, "password": "wrongA1"}
    )
    assert response.status_code == 401
