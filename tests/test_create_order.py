import allure
import requests

from data import ResponseMessages
from urls import Urls


class TestCreateOrder:
    @allure.step("Создать заказ")
    def create_order(self, ingredients, token=None):
        headers = {"Authorization": token} if token else {}
        return requests.post(
            Urls.ORDERS_URL, json={"ingredients": ingredients}, headers=headers, timeout=45
        )

    @allure.title("Авторизованный пользователь создает заказ с ингредиентами")
    def test_create_order_with_authorization(self, registered_user, ingredient_ids):
        response = self.create_order(ingredient_ids, registered_user["accessToken"])

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["order"]["number"], int)
        assert response.json()["order"]["number"] > 0

    @allure.title("Создание заказа без авторизации запрещено")
    def test_create_order_without_authorization(self, ingredient_ids):
        response = self.create_order(ingredient_ids)

        assert response.status_code == 401

    @allure.title("Заказ без ингредиентов отклоняется")
    def test_create_order_without_ingredients(self, registered_user):
        response = self.create_order([], registered_user["accessToken"])

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": ResponseMessages.NO_INGREDIENTS}

    @allure.title("Неверный хеш ингредиента возвращает ошибку")
    def test_create_order_with_invalid_hash(self, registered_user):
        response = self.create_order(["invalid_hash"], registered_user["accessToken"])

        assert response.status_code == 500
