from app.models import subject
from app.schemas.subject import Subject
from fastapi import responses
from sqlalchemy.orm import Session
from ..main import app, setup_db_config
from fastapi.testclient import TestClient
from ..db.connection import SessionLocal, engine
from ..db.base import Base
import pytest
from dotenv import load_dotenv
from base64 import b64decode
from ..models import User, Subject, ConfigValue
from jose import jwt
from ..core.config import ACCESS_TOKEN_SECRET
from ..core.security import gen_access_token, get_password_hash
from ..schemas import UserCreate, SubjectBase, Category
import json
from time import sleep

client = TestClient(app)
load_dotenv("../../dev.env")


@pytest.fixture(scope="function", autouse=True)
def prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    setup_db_config()


@pytest.fixture
def db():
    return SessionLocal()


@pytest.fixture
def create_user_data():
    user_dict = {
        "email": "testing@ucu.edu.ua",
        "password": "qwerty123A!",
        "repeat_password": "qwerty123A!",
    }
    return UserCreate(**user_dict)


@pytest.fixture
def create_subject_data():
    subject_dict = {
        "name": "Емоційний інтелект",
        "description": "Опис",
        "tutor": "Галина Іванівна",
        "category": "Люди і я",
        "max_students_count": 10,
    }
    return SubjectBase(**subject_dict)


@pytest.fixture
def register_user(db: Session, create_user_data: UserCreate):
    db_user = User(
        email=create_user_data.email,
        hashed_password=get_password_hash(create_user_data.password),
    )
    db.add(db_user)
    db.commit()
    return db_user


@pytest.fixture
def gen_user_auth_header(register_user):
    token = gen_access_token(register_user.id, 30)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def get_admin_user(db: Session, register_user):
    make_user_admin(db, register_user)
    return register_user


def make_user_admin(db: Session, db_user: User):
    db_user.is_admin = True
    db.add(db_user)
    db.commit()


@pytest.fixture
def get_db_subject(db: Session, create_subject_data):
    return create_db_subject(db, create_subject_data)


def create_db_subject(db, data):
    db_subject = Subject(**data.dict())
    db.add(db_subject)
    db.commit()
    return db_subject


@pytest.fixture
def create_many_subjects(create_subject_data, db: Session):
    categories = [
        Category.GOD_AND_I,
        Category.GOD_AND_I,
        Category.PEOPLE_AND_I,
        Category.PEOPLE_AND_I,
        Category.WORLD_AND_I,
        Category.WORLD_AND_I,
    ]
    subjects = []
    for idx, value in enumerate(categories):
        create_subject_data.name = "test" + str(idx)
        create_subject_data.category = value
        db_subjects = create_db_subject(db, create_subject_data)
        subjects.append(db_subjects)

    return subjects


def test_register_success(create_user_data):
    response = client.post("/register", json=create_user_data.dict())
    assert response.status_code == 201
    assert {"access_token", "token_type"} <= set(response.json().keys())


def test_register_wrong_email_domain(create_user_data):
    response = client.post(
        "/register", json={**create_user_data.dict(), "email": "testing@gmail.com"}
    )
    assert response.status_code == 400


def test_register_weak_password(create_user_data):
    password = "qwerty"
    response = client.post(
        "/register",
        json={
            **create_user_data.dict(),
            "password": password,
            "repeat_password": password,
        },
    )
    assert response.status_code == 400


def test_register_passwords_not_match(create_user_data):
    response = client.post(
        "/register",
        json={
            **create_user_data.dict(),
            "repeat_password": create_user_data.password + "not",
        },
    )
    assert response.status_code == 400


def test_login_success(create_user_data: UserCreate, register_user: User, db: Session):
    response = client.post(
        "/login",
        data={
            "username": create_user_data.email,
            "password": create_user_data.password,
        },
    )
    data = response.json()
    assert response.status_code == 200

    decoded_token = jwt.decode(data["access_token"], key=ACCESS_TOKEN_SECRET)

    db_user = db.query(User).filter_by(email=create_user_data.email).one()
    assert decoded_token["user_id"] == db_user.id


def test_login_incorrect_credentials(create_user_data: UserCreate, register_user: User):
    response = client.post(
        "/login",
        data={
            "username": create_user_data.email,
            "password": create_user_data.password + "not",
        },
    )
    assert response.status_code == 401


def test_public_user_cannot_access_protected_path():
    response = client.get("/user/subjects")
    assert response.status_code == 401


def test_logged_user_can_access_protected_path(gen_user_auth_header: dict):
    response = client.get("/user/subjects", headers=gen_user_auth_header)
    assert response.status_code == 200


def test_not_admin_cannot_access_protected_path(gen_user_auth_header: dict):
    response = client.post("/admin/subject/create", headers=gen_user_auth_header)
    assert response.status_code == 403


def test_admin_can_add_subject(
    get_admin_user: User,
    gen_user_auth_header,
    create_subject_data: SubjectBase,
    db: Session,
):
    data = create_subject_data.dict()
    response = client.post(
        "/admin/subject/create",
        headers=gen_user_auth_header,
        json=data,
    )
    assert response.status_code == 201
    assert db.query(Subject).first()


def test_admin_can_update_subject(
    get_admin_user: User,
    get_db_subject: Subject,
    gen_user_auth_header,
    db: Session,
    create_subject_data: SubjectBase,
):
    mock_data = "JUST_TESTING"
    create_subject_data.name = mock_data
    create_subject_data.description = mock_data
    response = client.put(
        f"/admin/subject/{get_db_subject.id}",
        headers=gen_user_auth_header,
        json=create_subject_data.dict(),
    )
    assert response.status_code == 200
    db.refresh(get_db_subject)

    assert get_db_subject.name == mock_data
    assert get_db_subject.description == mock_data


def test_admin_can_delete_subject(
    get_admin_user: User, gen_user_auth_header, db: Session, get_db_subject: Subject
):
    response = client.delete(
        f"/admin/subject/{get_db_subject.id}", headers=gen_user_auth_header
    )
    assert response.status_code == 200

    assert db.query(Subject).filter_by(id=get_db_subject.id).count() == 0


def test_admin_can_update_config(
    get_admin_user: User, gen_user_auth_header, db: Session
):
    response = client.patch(
        f"/admin/config",
        headers=gen_user_auth_header,
        json={"registration_opened": True},
    )
    assert response.status_code == 200
    db_config_value = db.query(ConfigValue).filter_by(prop="registration_opened").one()

    assert bool(db_config_value.value) == True


def test_user_can_get_subjects_1(
    db: Session,
    create_subject_data: SubjectBase,
    gen_user_auth_header,
    create_many_subjects,
):
    # 1) nothing choose -> show all subjects
    # 2) one choosen -> show only that category
    # 3) two choose -> cannot choose anymore

    response = client.get("/user/subjects", headers=gen_user_auth_header)
    assert response.status_code == 200
    assert len(response.json()) == len(create_many_subjects)


def test_user_can_get_subjects_2(
    db: Session,
    register_user: User,
    gen_user_auth_header,
    create_many_subjects,
):
    # 1) nothing choose -> show all subjects
    # 2) one choosen -> show only that category
    # 3) two choose -> cannot choose anymore
    choosen_subject = create_many_subjects.pop()
    register_user.subjects.append(choosen_subject)
    db.commit()

    response = client.get("/user/subjects", headers=gen_user_auth_header)
    assert response.status_code == 200
    for i in response.json():
        assert i["category"] == choosen_subject.category


def test_user_can_get_subjects_3(
    db: Session,
    register_user: User,
    gen_user_auth_header,
    create_many_subjects,
):
    # 1) nothing choose -> show all subjects
    # 2) one choosen -> show only that category
    # 3) two choose -> cannot choose anymore
    for _ in range(2):
        choosen_subject = create_many_subjects.pop()
        register_user.subjects.append(choosen_subject)

    db.commit()

    response = client.get("/user/subjects", headers=gen_user_auth_header)
    assert response.status_code == 400


def test_user_can_choose_subjects(
    register_user: User, gen_user_auth_header, db: Session, create_many_subjects
):
    get_ids = lambda items: list(map(lambda i: i.id, items))
    subject_ids = get_ids(create_many_subjects[:2])
    response = client.post(
        "/user/subjects/choose",
        headers=gen_user_auth_header,
        json={"subject_ids": subject_ids},
    )

    assert response.status_code == 200
    db.refresh(register_user)
    assert set(get_ids(register_user.subjects)) == set(subject_ids)
