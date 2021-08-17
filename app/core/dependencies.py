from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from ..db.connection import SessionLocal
from .security import oauth2_scheme
from ..core.config import ACCESS_TOKEN_SECRET
from jose import jwt
from ..crud.user import get_user_by_id
from ..models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # process token
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Invalid credentials"
    )
    try:
        decoded_token = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        user_id: str = decoded_token.get("user_id")
        if not user_id:
            raise credentials_exception
    except JWTError as err:
        print(err)
        raise credentials_exception

    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise credentials_exception
    return db_user


def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No don't have permission to access this page"
        )
    return current_user
