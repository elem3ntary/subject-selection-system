from app.schemas import user
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from .config import ACCESS_TOKEN_SECRET
from fastapi.security import OAuth2PasswordBearer, oauth2
from jose import jwt
from ..crud.user import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def gen_access_token(user_id: str, expire_in_minutes: int):
    exp = datetime.utcnow() + timedelta(minutes=expire_in_minutes)
    data = {"user_id": user_id, "exp": exp}
    access_token = jwt.encode(data, ACCESS_TOKEN_SECRET)
    return access_token


def authenticate_user(db: Session, email, password):
    db_user = get_user_by_email(db, email)
    if not user or not verify_password(password, db_user.hashed_password):
        return False
    return db_user
