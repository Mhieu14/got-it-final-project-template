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


def test_signup_invalid_body(client):
    # missing password
    response = client.post("/users/signup", json={"email": default_email})
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # missing email
    response = client.post("/users/signup", json={"password": default_password})
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # email invalid format
    response = client.post(
        "/users/signup", json={"email": "email", "password": default_password}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # email too long
    very_long_text = "".join("a" for i in range(255))
    response = client.post(
        "/users/signup",
        json={"email": f"{very_long_text}@email.com", "password": default_password},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # password too short
    response = client.post(
        "/users/signup", json={"email": default_email, "password": "shoR1"}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # password invalid format
    response = client.post(
        "/users/signup", json={"email": default_email, "password": "invalidpassword"}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001


def test_signup_email_existed(client):
    request_body = {"email": default_email, "password": default_password}
    client.post("/users/signup", json=request_body)
    response = client.post("/users/signup", json=request_body)
    assert response.status_code == 400
    assert response.json["error_code"] == 400000


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
    assert response.json["error_code"] == 400001

    # missing password
    response = client.post("/users/login", json={"email": default_email})
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

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


# def test_sign_up_email_exist(client, session):
#     init_user(session, number_of_user=2)
#     request_body = {"email": "email1@email.com", "password": "passwordA1"}
#     response = client.post("/users/signup", json=request_body)
#     assert response.status_code == 400
#     assert response.json["error_code"] == 400000
