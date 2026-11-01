import random
import string

import allure
import requests

from urls import Urls


def generate_random_string(length=15):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_user_data():
    return {
        "email": "qa_" + generate_random_string() + "@example.com",
        "password": generate_random_string(),
        "name": generate_random_string(),
    }


@allure.step("Удалить созданного тестового пользователя")
def delete_user(data):
    response = requests.post(
        Urls.LOGIN_URL,
        json={"email": data["email"], "password": data["password"]},
        timeout=30,
    )
    if response.status_code == 401:
        return
    assert response.status_code == 200
    token = response.json()["accessToken"]
    response = requests.delete(
        Urls.USER_URL, headers={"Authorization": token}, timeout=30
    )
    assert response.status_code == 202
