import requests
import pytest


BASE_URL = "https://ru.yougile.com/api-v2/projects"
API_TOKEN = (
    "C+c3vxQ3zCFxMF6447D1QBg+6hIZUa5cw2T2jHB-YHkg3wQg+x26a+PqWK5zVWIy"
)


@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}",
    }


@pytest.fixture
def invalid_headers():
   return {
        "Content-Type": "application/json",
        "Authorization": "Bearer INVALID_TOKEN",
    }


@pytest.fixture
def payload():
    return {
        "title": "Secret",
        "users": {
            "b6aa4400-8e6d-4212-8b8e-3639b7c02ca9": "worker",
        },
    }


def test_create_project_success(headers, payload):
    response = requests.post(BASE_URL, json=payload, headers=headers)
    assert response.status_code == 201, f"Ошибка: {response.text}"


def test_create_project_invalid_token(invalid_headers, payload):
    response = requests.post(BASE_URL, json=payload, headers=invalid_headers)
    assert response.status_code == 401, f"Ошибка: {response.text}"