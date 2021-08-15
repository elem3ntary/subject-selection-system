from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserLogin
from ..core.dependencies import get_db
from ..models import User
from ..core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.security import (
    authenticate_user,
    get_password_hash,
    gen_access_token,
    oauth2_scheme,
)
from ..crud.user import get_user_by_email, create_user, get_user_by_id
from fastapi.security import OAuth2PasswordRequestForm
import re

router = APIRouter(tags=["public"])


@router.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    access_token = gen_access_token(db_user.id, ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # if domain -> error
    domain_regex = ".+@ucu.edu.ua"
    if not re.match(domain_regex, user.email):
        raise HTTPException(400, "Only ucu.edu.ua emails are allowerd")
    # get if user exists
    db_user = get_user_by_email(db, user.email)
    # if true -> error
    if db_user:
        raise HTTPException(400, "Email is already used")
    # Check if passwords match
    if not user.password == user.repeat_password:
        raise HTTPException(400, "Passwords don`t match")

    # hash user password
    hashed_password = get_password_hash(user.password)
    # register user
    db_user = create_user(db, user.email, hashed_password)
    # gen token
    access_token = gen_access_token(db_user.id, ACCESS_TOKEN_EXPIRE_MINUTES)

    return {"access_token": access_token, "token_type": "bearer"}
