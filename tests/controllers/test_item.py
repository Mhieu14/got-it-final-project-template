import pytest

from main.commons.exceptions import BadRequest, Forbidden, NotFound, ValidationError
from main.constants import (
    DESCRIPTION_MAX_LENGTH,
    LIMIT_DEFAULT,
    NAME_MAX_LENGTH,
    OFFSET_DEFAULT,
)
from tests.utils.init_data import (
    create_categories,
    create_category,
    create_item,
    create_items,
    create_user,
    create_users,
    generate_auth_headers,
)

default_name = "item default_name"
default_description = "item default_description"


def test_create_item_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
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


def test_create_item_not_found_category(client):
    user = create_user()
    category = create_category(user_id=user.id)
    headers = generate_auth_headers(user.id)
    request_body = {"name": default_name, "description": default_description}
    response = client.post(
        f"/categories/{category.id + 1}/items", json=request_body, headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


@pytest.mark.parametrize(
    "request_body",
    [
        None,
        {},
        {"name": default_name},
        {"description": default_description},
        {"name": "a" * (NAME_MAX_LENGTH + 1), "description": default_description},
        {"name": default_name, "description": "a" * (DESCRIPTION_MAX_LENGTH + 1)},
    ],
)
def test_create_item_invalid_body(client, request_body):
    user = create_user()
    category = create_category(user_id=user.id)
    headers = generate_auth_headers(user.id)
    response = client.post(
        f"/categories/{category.id}/items", headers=headers, json=request_body
    )
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code


def test_create_item_duplicate_name(client):
    user = create_user()
    category = create_category(user_id=user.id)
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
    assert response.json["error_code"] == BadRequest.error_code


def test_get_list_item_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    number_of_items = 30
    create_items(
        user_id=user.id, category_id=category.id, number_of_items=number_of_items
    )
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id}/items", headers=headers)
    assert response.status_code == 200
    assert "items" in response.json
    assert "pagination" in response.json
    first_item = response.json["items"][0]
    assert "id" in first_item
    assert "name" in first_item
    assert "description" not in first_item
    assert "user_id" in first_item
    assert len(response.json["items"]) == LIMIT_DEFAULT
    assert response.json["pagination"]["total"] == number_of_items
    assert response.json["pagination"]["offset"] == OFFSET_DEFAULT
    assert response.json["pagination"]["limit"] == LIMIT_DEFAULT

    response = client.get(
        f"/categories/{category.id}/items",
        query_string={"offset": 20},
        headers=headers,
    )
    assert len(response.json["items"]) == number_of_items - 20
    assert response.json["pagination"]["total"] == number_of_items
    assert response.json["pagination"]["offset"] == 20
    assert response.json["pagination"]["limit"] == LIMIT_DEFAULT

    response = client.get(
        f"/categories/{category.id}/items",
        query_string={"limit": 10},
        headers=headers,
    )
    assert len(response.json["items"]) == 10
    assert response.json["pagination"]["total"] == number_of_items
    assert response.json["pagination"]["offset"] == OFFSET_DEFAULT
    assert response.json["pagination"]["limit"] == 10


def test_get_list_item_not_found_category(client):
    user = create_user()
    category = create_category(user_id=user.id)
    create_items(user_id=user.id, category_id=category.id, number_of_items=10)
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id + 1}/items", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_get_one_item_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
    headers = generate_auth_headers(user.id)

    response = client.get(f"/categories/{category.id}/items/{item.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == item.id
    assert response.json["name"] == item.name
    assert response.json["description"] == item.description
    assert response.json["user_id"] == item.user_id
    assert response.json["category_id"] == item.category_id


def test_get_one_item_not_found(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.get(
        f"/categories/{category.id}/items/{item.id + 1}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code

    # wrong category, right item
    response = client.get(
        f"/categories/{category.id + 1}/items/{item.id}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_delete_item_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(
        f"/categories/{category.id}/items/{item.id}", headers=headers
    )
    assert response.status_code == 200


def test_delete_item_not_found(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.delete(
        f"/categories/{category.id}/items/{item.id + 1}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code

    # wrong category, right item
    response = client.delete(
        f"/categories/{category.id + 1}/items/{item.id}", headers=headers
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_delete_item_forbidden(client):
    users = create_users(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = create_categories(user_id=user_id_create, number_of_categories=1)[0]
    item = create_items(
        user_id=user_id_create,
        category_id=category.id,
        number_of_items=1,
    )[0]
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.delete(
        f"/categories/{category.id}/items/{item.id}", headers=headers
    )
    assert response.status_code == 403
    assert response.json["error_code"] == Forbidden.error_code


def test_update_item_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
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


def test_update_item_not_found(client):
    user = create_user()
    category = create_category(user_id=user.id)
    item = create_item(user_id=user.id, category_id=category.id)
    headers = generate_auth_headers(user_id=user.id)

    # right category, wrong item
    response = client.put(
        f"/categories/{category.id}/items/{item.id + 1}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code

    # wrong category, right item
    response = client.put(
        f"/categories/{category.id + 1}/items/{item.id}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_update_item_forbidden(client):
    users = create_users(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = create_categories(user_id=user_id_create, number_of_categories=1)[0]
    item = create_items(
        user_id=user_id_create, category_id=category.id, number_of_items=1
    )[0]
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.put(
        f"/categories/{category.id}/items/{item.id}",
        json={"name": default_name, "description": default_description},
        headers=headers,
    )
    assert response.status_code == 403
    assert response.json["error_code"] == Forbidden.error_code


def test_update_item_duplicate_name(client):
    user = create_user()
    category = create_category(user_id=user.id)
    items = create_items(user_id=user.id, category_id=category.id, number_of_items=2)
    headers = generate_auth_headers(user.id)
    response = client.put(
        f"/categories/{category.id}/items/{items[1].id}",
        json={"name": items[0].name, "description": "a different des"},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json["error_code"] == BadRequest.error_code
