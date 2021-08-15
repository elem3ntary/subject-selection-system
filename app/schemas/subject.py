from enum import Enum
from typing import List
from pydantic import BaseModel


class Category(Enum):
    GOD_AND_I = "Бог і я"
    WORLD_AND_I = "Світ і я"
    PEOPLE_AND_I = "Люди і я"


class SubjectBase(BaseModel):
    name: str
    description: str
    tutor: str
    category: Category
    max_students_count: int


class Subject(SubjectBase):
    id: int
    students: List["User"]

    class Config:
        orm_mode = True
