import pytest
import requests


BASE_URL = "https://ru.yougile.com/api-v2/projects/a8162442-9346-4900-9512-59c743d0371b"

API_TOKEN = "C+c3vxQ3zCFxMF6447D1QBg+6hIZUa5cw2T2jHB-YHkg3wQg+x26a+PqWK5zVWIy"


@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }


@pytest.fixture
def invalid_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer INVALID_TOKEN"
    }


def test_create_project_success(headers):
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 200, f"Ошибка: {response.text}"


def test_create_project_invalid_token(invalid_headers):
    response = requests.post(BASE_URL, headers=invalid_headers)
    assert response.status_code == 401, f"Ошибка: {response.text}"