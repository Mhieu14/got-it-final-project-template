from tests.utils.init_data import generate_auth_headers

default_name = "cate0_email0"
default_description = "Category 0 description"


def test_create_category_success(client):
    request_body = {"name": default_name, "description": default_description}
    headers = generate_auth_headers()
    response = client.post("/categories", json=request_body, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["name"] == default_name
    assert response.json["description"] == default_description
    assert "user_id" in response.json
    assert "created_at" in response.json
    assert "updated_at" in response.json


def test_create_category_fail(client):
    headers = generate_auth_headers()
    # missing name
    response = client.post("/categories", json={"name": default_name}, headers=headers)
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # missing description
    response = client.post(
        "/categories", headers=headers, json={"description": default_description}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # name too long
    very_long_name = "".join("a" for i in range(256))
    response = client.post(
        "/categories",
        headers=headers,
        json={"name": very_long_name, "description": default_description},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # description too long
    very_long_des = "".join("a" for i in range(5001))
    response = client.post(
        "/categories",
        headers=headers,
        json={"name": default_name, "description": very_long_des},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001
