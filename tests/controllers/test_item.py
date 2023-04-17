from tests.utils.init_data import (
    generate_auth_headers,
    init_category,
    init_item,
    init_user,
)

default_name = "item default_name"
default_description = "item default_description"


def test_create_item_success(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user.id)
    request_body = {"name": default_name, "description": default_description}
    response = client.post(
        f"/categories/{category.id}/items", json=request_body, headers=headers
    )
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["name"] == default_name
    assert response.json["description"] == default_description
    assert response.json["category_id"] == category.id
    assert response.json["user_id"] == user.id


def test_create_item_notfound_category(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user.id)
    request_body = {"name": default_name, "description": default_description}
    response = client.post(
        f"/categories/{category.id + 1}/items", json=request_body, headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_create_item_invalid_body(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user.id)
    # missing req body
    response = client.post(f"/categories/{category.id}/items", headers=headers)
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # missing name
    response = client.post(
        f"/categories/{category.id}/items", json={"name": default_name}, headers=headers
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # missing description
    response = client.post(
        f"/categories/{category.id}/items",
        headers=headers,
        json={"description": default_description},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # name too long
    very_long_name = "".join("a" for i in range(256))
    response = client.post(
        f"/categories/{category.id}/items",
        headers=headers,
        json={"name": very_long_name, "description": default_description},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    # description too long
    very_long_des = "".join("a" for i in range(5001))
    response = client.post(
        f"/categories/{category.id}/items",
        headers=headers,
        json={"name": default_name, "description": very_long_des},
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001


def test_create_item_duplicate_name(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    headers = generate_auth_headers(user.id)
    client.post(
        f"/categories/{category.id}/items",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    response = client.post(
        f"/categories/{category.id}/items",
        json={"name": default_name, "description": "a different des"},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400000


def test_get_list_item_success(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    init_item(user_id=user.id, category_id=category.id, number_of_item=30)
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id}/items", headers=headers)
    assert response.status_code == 200
    assert "items" in response.json
    assert "pagination" in response.json
    first = response.json["items"][0]
    assert "id" in first
    assert "name" in first
    assert "description" not in first
    assert "user_id" in first
    assert len(response.json["items"]) == 20
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 0
    assert response.json["pagination"]["limit"] == 20

    response = client.get(f"/categories/{category.id}/items?offset=20", headers=headers)
    assert len(response.json["items"]) == 10
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 20
    assert response.json["pagination"]["limit"] == 20

    response = client.get(f"/categories/{category.id}/items?limit=10", headers=headers)
    assert len(response.json["items"]) == 10
    assert response.json["pagination"]["total"] == 30
    assert response.json["pagination"]["offset"] == 0
    assert response.json["pagination"]["limit"] == 10


def test_get_list_item_notfound_category(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    init_item(user_id=user.id, category_id=category.id, number_of_item=10)
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id + 1}/items", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_get_one_item_success(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id}/items/{item.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == item.id
    assert response.json["name"] == item.name
    assert response.json["description"] == item.description
    assert response.json["user_id"] == item.user_id
    assert response.json["category_id"] == item.category_id


def test_get_one_item_notfound(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.get(
        f"/categories/{category.id}/items/{item.id + 1}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000

    # wrong category, right item
    response = client.get(
        f"/categories/{category.id + 1}/items/{item.id}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_delete_item_success(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(
        f"/categories/{category.id}/items/{item.id}", headers=headers
    )
    assert response.status_code == 200


def test_delete_item_notfound(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.delete(
        f"/categories/{category.id}/items/{item.id + 1}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000

    # wrong category, right item
    response = client.delete(
        f"/categories/{category.id + 1}/items/{item.id}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_delete_item_forbidden(client):
    users = init_user(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = init_category(user_id=user_id_create, number_of_cate=1)[0]
    item = init_item(user_id=user_id_create, category_id=category.id, number_of_item=1)[
        0
    ]
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.delete(
        f"/categories/{category.id}/items/{item.id}", headers=headers
    )
    assert response.status_code == 403
    assert response.json["error_code"] == 403000


def test_update_item_success(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    response = client.put(
        f"/categories/{category.id}/items/{item.id}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["name"] == default_name
    assert response.json["description"] == default_description
    assert response.json["category_id"] == category.id
    assert response.json["user_id"] == user.id


def test_update_item_notfound(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    item = init_item(user_id=user.id, category_id=category.id, number_of_item=1)[0]
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.put(
        f"/categories/{category.id}/items/{item.id + 1}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000

    # wrong category, right item
    response = client.put(
        f"/categories/{category.id + 1}/items/{item.id}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json["error_code"] == 404000


def test_update_item_forbidden(client):
    users = init_user(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = init_category(user_id=user_id_create, number_of_cate=1)[0]
    item = init_item(user_id=user_id_create, category_id=category.id, number_of_item=1)[
        0
    ]
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.put(
        f"/categories/{category.id}/items/{item.id}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 403
    assert response.json["error_code"] == 403000


def test_update_item_duplicate_name(client):
    user = init_user(1)[0]
    category = init_category(user_id=user.id, number_of_cate=1)[0]
    items = init_item(user_id=user.id, category_id=category.id, number_of_item=2)
    headers = generate_auth_headers(user.id)
    response = client.put(
        f"/categories/{category.id}/items/{items[1].id}",
        json={"name": items[0].name, "description": "a different des"},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400000
