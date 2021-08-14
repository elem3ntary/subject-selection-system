from ..main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


@pytest.fixture
def correct_user_data():
    user_dict = dict(
        {
            "email": "testing@ucu.edu.ua",
            "password": "qwerty123A!",
            "repeat_password": "qwerty123A!",
        },
    )
    return user_dict


def test_register_success(correct_user_data):
    response = client.post("/register", json=correct_user_data)
    assert response.status_code == 200
    assert {"access_token", "token_type"} <= set(response.json().keys())


def test_register_wrong_email_domain(correct_user_data):
    response = client.post(
        "/register", json={**correct_user_data, "email": "testing@gmail.com"}
    )
    assert response.status_code == 400


def test_register_weak_password(correct_user_data):
    password = "qwerty"
    response = client.post(
        "/register",
        json={**correct_user_data, "password": password, "repeat_password": password},
    )
    assert response.status_code == 400


def test_register_passwords_dont_match(correct_user_data):
    response = client.post(
        "/register",
        json={
            **correct_user_data,
            "repeat_password": correct_user_data["password"] + "not",
        },
    )
    assert response.status_code == 400
