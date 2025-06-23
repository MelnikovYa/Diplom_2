import pytest
import requests
import allure

@allure.epic("User API")
class TestUserAPI:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, base_url, random_user):
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(f"{base_url}/api/auth/register", json=random_user)
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание пользователя с уже существующим email")
    def test_create_duplicate_user(self, base_url, register_user):
        with allure.step("Повторная регистрация того же пользователя"):
            response = requests.post(f"{base_url}/api/auth/register", json=register_user)
        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без одного обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, base_url, random_user, missing_field):
        user = random_user.copy()
        user.pop(missing_field)
        with allure.step(f"Создание пользователя без поля {missing_field}"):
            response = requests.post(f"{base_url}/api/auth/register", json=user)
        with allure.step("Проверка ошибки 403"):
            assert response.status_code == 403

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_valid_user(self, base_url, register_user):
        with allure.step("Вход с корректными email и паролем"):
            response = requests.post(f"{base_url}/api/auth/login", json=register_user)
        with allure.step("Проверка 200 OK и accessToken"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Ошибка при входе с неверными логином и паролем")
    @pytest.mark.parametrize("field, value", [
        ("email", "wrong@example.com"),
        ("password", "wrongpassword123")
    ])
    def test_login_invalid_credentials(self, base_url, register_user, field, value):
        wrong_user = register_user.copy()
        wrong_user[field] = value
        with allure.step(f"Вход с неверным полем: {field}"):
            response = requests.post(f"{base_url}/api/auth/login", json=wrong_user)
        with allure.step("Проверка ошибки 401"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"