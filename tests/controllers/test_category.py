from tests.utils.init_data import (
    count_items_in_category,
    generate_auth_headers,
    init_category,
    init_item,
    init_users,
)

default_name = "cate0"
default_description = "Category 0 description"


def test_create_category_success(client):
    request_body = {"name": default_name, "description": default_description}
    user = init_users(number_of_user=1)[0]
    headers = generate_auth_headers(user.id)
    response = client.post("/categories", json=request_body, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["name"] == default_name
    assert response.json["description"] == default_description
    assert response.json["user_id"] == user.id


def test_create_category_invalid_body(client):
    user = init_users(number_of_user=1)[0]
    headers = generate_auth_headers(user.id)
    # missing req body
    response = client.post("/categories", headers=headers)
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

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


def test_create_category_duplicate_name(client):
    user = init_users(number_of_user=1)[0]
    headers = generate_auth_headers(user.id)
    client.post(
        "/categories",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    response = client.post(
        "/categories",
        json={"name": default_name, "description": "a different des"},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400000


def test_get_list_category_success(client):
    user = init_users(number_of_user=1)[0]
    init_category(user_id=user.id, number_of_cate=30)
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories", headers=headers)
    assert response.status_code == 200
    assert "categories" in response.json
    assert "pagination" in response.json
    first = response.json["categories"][0]
    assert "id" in first
    assert "name" in first
    assert "description" not in first
    assert "user_id" in first
    assert len(response.json["categories"]) == 20
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 0
    assert response.json["pagination"]["limit"] == 20

    response = client.get("/categories?offset=20", headers=headers)
    assert len(response.json["categories"]) == 10
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 20
    assert response.json["pagination"]["limit"] == 20

    response = client.get("/categories?limit=10", headers=headers)
    assert len(response.json["categories"]) == 10
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 0
    assert response.json["pagination"]["limit"] == 10


def test_get_list_category_invalid_params(client):
    user = init_users(number_of_user=1)[0]
    init_category(user_id=user.id, number_of_cate=30)
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories?limit=a", headers=headers)
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    response = client.get("/categories?offset=-1", headers=headers)
    assert response.status_code == 400
    assert response.json["error_code"] == 400001


def test_get_one_category_success(client):
    user = init_users(number_of_user=1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    response = client.get(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == category.id
    assert response.json["name"] == category.name
    assert response.json["description"] == category.description
    assert response.json["user_id"] == category.user_id


def test_get_one_category_not_found(client):
    user = init_users(number_of_user=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories/1", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_delete_category_success(client):
    user = init_users(number_of_user=1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    init_item(user_id=user.id, category_id=category.id, number_of_item=30)
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 200
    assert count_items_in_category(category_id=category.id) == 0


def test_delete_category_notfound(client):
    user = init_users(number_of_user=1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(f"/categories/{category.id + 1}", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_delete_category_forbidden(client):
    users = init_users(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = init_category(user_id=user_id_create, number_of_cate=1)[0]
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.delete(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 403
    assert response.json["error_code"] == 403000
