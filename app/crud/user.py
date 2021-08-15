from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter_by(email=email).one_or_none()


def get_user_by_id(db: Session, id):
    return db.query(User).filter_by(id=id).one_or_none()


def create_user(db: Session, email, hashed_password) -> User:
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return user
