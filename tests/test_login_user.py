import allure
import pytest

from data import ResponseMessages
from helpers import generate_random_string
from helpers import login_user


class TestLoginUser:

    @allure.title("Вход существующего пользователя")
    def test_login_existing_user(self, registered_user):
        response = login_user({key: registered_user[key] for key in ["email", "password"]})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": registered_user["email"], "name": registered_user["name"]}
        assert body["accessToken"]
        assert body["refreshToken"]

    @allure.title("Неверные данные не позволяют войти")
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_login_invalid_credentials(self, registered_user, field):
        credentials = {key: registered_user[key] for key in ["email", "password"]}
        credentials[field] = generate_random_string() + ("@example.com" if field == "email" else "")

        response = login_user(credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": ResponseMessages.INVALID_CREDENTIALS}
