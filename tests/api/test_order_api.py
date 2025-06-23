import pytest
import requests
import allure

@allure.epic("Order API")
class TestOrderAPI:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(self, base_url, access_token, ingredient_hashes):
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"ingredients": ingredient_hashes}
        with allure.step("Создание заказа авторизованным пользователем"):
            response = requests.post(f"{base_url}/api/orders", json=data, headers=headers)
        with allure.step("Проверка 200 OK"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, base_url, ingredient_hashes):
        data = {"ingredients": ingredient_hashes}
        with allure.step("Создание заказа без токена"):
            response = requests.post(f"{base_url}/api/orders", json=data)
        with allure.step("Проверка 200 OK — не требует токен"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, base_url, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"ingredients": []}
        with allure.step("Создание заказа с пустым списком ингредиентов"):
            response = requests.post(f"{base_url}/api/orders", json=data, headers=headers)
        with allure.step("Проверка ошибки 400"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_invalid_ingredients(self, base_url, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"ingredients": ["invalid_hash"]}
        with allure.step("Создание заказа с невалидным ингредиентом"):
            response = requests.post(f"{base_url}/api/orders", json=data, headers=headers)
        with allure.step("Проверка ошибки 500 или специфики API"):
            assert response.status_code in [400, 500]
