from app.schemas.subject import Category
from ..db.connection import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relation
from .user import association_table


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True, unique=True)
    description = Column(String(255), index=True)
    tutor = Column(String(50), index=True)
    category = Column(String(20), index=True)

    max_students_count = Column(Integer)
    students = relation("User", secondary=association_table, back_populates="subjects")
