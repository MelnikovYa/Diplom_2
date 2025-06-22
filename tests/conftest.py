import pytest
import requests
from utils.urls import BASE_URL
from utils.helpers import generate_random_user

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def random_user():
    return generate_random_user()

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
