import pytest
import requests

from helpers import delete_user, generate_user_data
from urls import Urls


@pytest.fixture
def user_data():
    data = generate_user_data()
    yield data
    delete_user(data)


@pytest.fixture
def registered_user(user_data):
    response = requests.post(Urls.REGISTER_URL, json=user_data, timeout=30)
    assert response.status_code == 200
    data = user_data.copy()
    data["accessToken"] = response.json()["accessToken"]
    return data


@pytest.fixture
def ingredient_ids():
    response = requests.get(Urls.INGREDIENTS_URL, timeout=30)
    assert response.status_code == 200
    ingredients = response.json()["data"]
    bun = None
    filling = None
    for item in ingredients:
        if item["type"] == "bun" and bun is None:
            bun = item["_id"]
        if item["type"] == "main" and filling is None:
            filling = item["_id"]
    assert bun is not None
    assert filling is not None
    return [bun, filling, bun]
