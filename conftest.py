import pytest

from helpers import delete_user, generate_user_data, create_user, get_ingredients


@pytest.fixture
def user_data():
    data = generate_user_data()
    yield data
    delete_user(data)


@pytest.fixture
def registered_user(user_data):
    response = create_user(user_data)
    response.raise_for_status()
    data = user_data.copy()
    data["accessToken"] = response.json()["accessToken"]
    return data


@pytest.fixture
def ingredient_ids():
    ingredients = get_ingredients()
    bun = None
    filling = None
    for item in ingredients:
        if item["type"] == "bun" and bun is None:
            bun = item["_id"]
        if item["type"] == "main" and filling is None:
            filling = item["_id"]
    if bun is None or filling is None:
        raise ValueError("Не удалось подготовить заказ: нет булки или начинки")
    return [bun, filling, bun]
