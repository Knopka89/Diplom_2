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
    response = login_user({"email": data["email"], "password": data["password"]})
    if response.status_code == 401:
        return
    response.raise_for_status()
    token = response.json()["accessToken"]
    response = requests.delete(
        Urls.USER_URL, headers={"Authorization": token}, timeout=30
    )
    response.raise_for_status()


@allure.step("Создать заказ")
def create_order(ingredients, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.post(
        Urls.ORDERS_URL, json={"ingredients": ingredients}, headers=headers, timeout=45
    )


@allure.step("Создать пользователя")
def create_user(payload):
    return requests.post(Urls.REGISTER_URL, json=payload, timeout=30)


@allure.step("Авторизовать пользователя")
def login_user(credentials):
    return requests.post(Urls.LOGIN_URL, json=credentials, timeout=30)


@allure.step("Получить ингредиенты для тестового заказа")
def get_ingredients():
    response = requests.get(Urls.INGREDIENTS_URL, timeout=30)
    response.raise_for_status()
    return response.json()["data"]
