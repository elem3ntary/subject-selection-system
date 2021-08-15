from pydantic import BaseModel
from typing import List
from .subject import Subject


class UserBase(BaseModel):
    email: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    repeat_password: str


class User(UserBase):
    id: int
    is_admin: bool
    subjects: List[Subject]

    class Config:
        orm_mode = True
