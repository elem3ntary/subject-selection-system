from sqlalchemy.orm import Session
from ..main import app
from fastapi.testclient import TestClient
from ..db.connection import SessionLocal, engine
from ..db.base import Base
import pytest
from dotenv import load_dotenv
from base64 import b64decode
from ..models import User
from jose import jwt
from ..core.config import ACCESS_TOKEN_SECRET
import json

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv("../../dev.env")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    return SessionLocal()


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
    print(response.json())
    assert response.status_code == 201
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


def test_register_passwords_not_match(correct_user_data):
    response = client.post(
        "/register",
        json={
            **correct_user_data,
            "repeat_password": correct_user_data["password"] + "not",
        },
    )
    assert response.status_code == 400


def test_login_success(correct_user_data, db: Session):
    response = client.post(
        "/login",
        data={
            "username": correct_user_data["email"],
            "password": correct_user_data["password"],
        },
    )
    data = response.json()
    assert response.status_code == 200

    decoded_token = jwt.decode(data["access_token"], key=ACCESS_TOKEN_SECRET)

    db_user = db.query(User).filter_by(email=correct_user_data["email"]).one()
    assert decoded_token["user_id"] == db_user.id


def test_login_incorrect_credentials(correct_user_data):
    response = client.post(
        "/login",
        data={
            "username": correct_user_data["email"],
            "password": correct_user_data["password"] + "not correct",
        },
    )
    assert response.status_code == 401
