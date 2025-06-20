import pytest
import random
import string
import requests


@pytest.fixture
def base_url():
    return "https://stellarburgers.nomoreparties.site"


@pytest.fixture
def random_user():
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
    return {
        "email": email,
        "password": "password123",
        "name": "Test User"
    }


@pytest.fixture
def register_user(base_url, random_user):
    requests.post(f"{base_url}/api/auth/register", json=random_user)
    return random_user


@pytest.fixture
def access_token(base_url, register_user):
    response = requests.post(f"{base_url}/api/auth/login", json=register_user)
    return response.json().get("accessToken").split("Bearer ")[-1]


@pytest.fixture
def ingredient_hashes(base_url):
    response = requests.get(f"{base_url}/api/ingredients")
    data = response.json()
    return [item["_id"] for item in data["data"][:2]]
