from typing import List
from sqlalchemy.sql.functions import count
from app.models.config_value import ConfigValue
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate
from sqlalchemy.exc import InvalidRequestError
from app.models import Subject, subject
from app.schemas import Category
from collections import Counter
from fastapi import HTTPException
from .subject import get_subject_by_id


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter_by(email=email).one_or_none()


def get_user_by_id(db: Session, id):
    return db.query(User).filter_by(id=id).one_or_none()


def create_user(db: Session, email, hashed_password) -> User:
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return user


def update_config(db: Session, props: dict):
    for prop, value in props.items():
        try:
            db.query(ConfigValue).filter_by(prop=prop).update({"value": value})
        except InvalidRequestError:
            return False
    db.commit()
    return True


def get_available_subjects(db: Session, user: User):
    # There are 3 categories
    # User can pick two subjects from the same category that he hasn`t picked yet

    # getting least common category
    choosen_categories = Counter(map(lambda i: i.category, user.subjects)).most_common(
        3
    )
    if len(choosen_categories) > 0:
        least_common_name, least_common_name_count = choosen_categories.pop()
        if least_common_name_count > 1:
            raise HTTPException(400, "You have choosen your subjects")
        available_categories = (
            db.query(Subject).filter(Subject.category == least_common_name).all()
        )
    else:
        available_categories = (
            db.query(Subject).filter(Subject.category not in choosen_categories).all()
        )

    return available_categories


def update_subjects(db: Session, subject_ids: List[int], current_user: User):
    for subject_id in subject_ids:
        subject = get_subject_by_id(db, subject_id)
        if not subject:
            raise HTTPException(400, f"Subject id {subject_id} is not valid")
        current_user.subjects.append(subject)
    db.commit()
