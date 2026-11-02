import allure
import pytest

from data import ResponseMessages
from helpers import create_user


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data):
        response = create_user(user_data)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": user_data["email"], "name": user_data["name"]}
        assert body["accessToken"]
        assert body["refreshToken"]

    @allure.title("Повторная регистрация пользователя запрещена")
    def test_create_existing_user(self, registered_user):
        payload = {key: registered_user[key] for key in ["email", "password", "name"]}
        response = create_user(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ResponseMessages.USER_ALREADY_EXISTS}

    @allure.title("Нельзя создать пользователя без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, user_data, field):
        payload = user_data.copy()
        payload[field] = ""

        response = create_user(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ResponseMessages.REQUIRED_FIELDS}
