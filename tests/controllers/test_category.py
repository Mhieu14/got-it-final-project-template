import pytest

from main.commons.exceptions import BadRequest, Forbidden, NotFound, ValidationError
from main.constants import (
    DESCRIPTION_MAX_LENGTH,
    LIMIT_DEFAULT,
    LIMIT_MAX,
    NAME_MAX_LENGTH,
    OFFSET_DEFAULT,
)
from tests.utils.init_data import (
    count_items_in_category,
    create_categories,
    create_category,
    create_items,
    create_user,
    create_users,
    generate_auth_headers,
)

default_name = "category default_name"
default_description = "category default_description"


def test_create_category_success(client):
    request_body = {
        "name": f"{' ' * 5}{default_name}{' ' * 5}",
        "description": f"{' ' * 5}{default_description}{' ' * 5}",
    }
    user = create_user()
    headers = generate_auth_headers(user.id)
    response = client.post("/categories", json=request_body, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json
    assert response.json["name"] == default_name
    assert response.json["description"] == default_description
    assert response.json["user_id"] == user.id


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
def test_create_category_invalid_body(client, request_body):
    user = create_user()
    headers = generate_auth_headers(user.id)
    response = client.post("/categories", headers=headers, json=request_body)
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code


def test_create_category_duplicate_name(client):
    user = create_user()
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
    assert response.json["error_code"] == BadRequest.error_code


def test_get_list_category_success(client):
    user = create_user()
    number_of_categories = 30
    create_categories(user_id=user.id, number_of_categories=number_of_categories)
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories", headers=headers)
    assert response.status_code == 200
    assert "categories" in response.json
    assert "pagination" in response.json
    first_category = response.json["categories"][0]
    assert "id" in first_category
    assert "name" in first_category
    assert "description" not in first_category
    assert "user_id" in first_category
    assert len(response.json["categories"]) == LIMIT_DEFAULT
    assert response.json["pagination"]["total"] == number_of_categories
    assert response.json["pagination"]["offset"] == OFFSET_DEFAULT
    assert response.json["pagination"]["limit"] == LIMIT_DEFAULT

    response = client.get("/categories", query_string={"offset": 20}, headers=headers)
    assert len(response.json["categories"]) == number_of_categories - 20
    assert response.json["pagination"]["total"] == number_of_categories
    assert response.json["pagination"]["offset"] == 20
    assert response.json["pagination"]["limit"] == LIMIT_DEFAULT

    response = client.get("/categories", query_string={"limit": 10}, headers=headers)
    assert len(response.json["categories"]) == 10
    assert response.json["pagination"]["total"] == number_of_categories
    assert response.json["pagination"]["offset"] == OFFSET_DEFAULT
    assert response.json["pagination"]["limit"] == 10


@pytest.mark.parametrize(
    "query_string",
    [
        {"offset": -1},
        {"limit": -1},
        {"offset": "a"},
        {"limit": "b"},
        {"limit": LIMIT_MAX + 1},
    ],
)
def test_get_list_category_invalid_params(client, query_string):
    user = create_user()
    create_categories(user_id=user.id, number_of_categories=30)
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories", headers=headers, query_string=query_string)
    assert response.status_code == 400
    assert response.json["error_code"] == ValidationError.error_code


def test_get_one_category_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    headers = generate_auth_headers(user_id=user.id)

    response = client.get(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == category.id
    assert response.json["name"] == category.name
    assert response.json["description"] == category.description
    assert response.json["user_id"] == category.user_id


def test_get_one_category_not_found(client):
    user = create_user()
    headers = generate_auth_headers(user_id=user.id)

    response = client.get("/categories/1", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_delete_category_success(client):
    user = create_user()
    category = create_category(user_id=user.id)
    create_items(user_id=user.id, category_id=category.id, number_of_items=30)
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 200
    assert count_items_in_category(category_id=category.id) == 0


def test_delete_category_not_found(client):
    user = create_user()
    category = create_category(user_id=user.id)
    headers = generate_auth_headers(user_id=user.id)

    response = client.delete(f"/categories/{category.id + 1}", headers=headers)
    assert response.status_code == 404
    assert response.json["error_code"] == NotFound.error_code


def test_delete_category_forbidden(client):
    users = create_users(2)
    user_id_create = users[0].id
    user_id_delete = users[1].id
    category = create_category(user_id=user_id_create)
    headers = generate_auth_headers(user_id=user_id_delete)

    response = client.delete(f"/categories/{category.id}", headers=headers)
    assert response.status_code == 403
    assert response.json["error_code"] == Forbidden.error_code
