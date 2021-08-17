from enum import Enum
from typing import List
from pydantic import BaseModel


class Category(str, Enum):
    GOD_AND_I = "Бог і я"
    WORLD_AND_I = "Світ і я"
    PEOPLE_AND_I = "Люди і я"


class SubjectBase(BaseModel):
    name: str
    description: str
    tutor: str
    category: Category
    max_students_count: int

    class Config:
        use_enum_values = True


class Subject(SubjectBase):
    id: int
    students: List

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
