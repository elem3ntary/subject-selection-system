from ..db.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relation


association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("subject_id", ForeignKey("subjects.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), index=True, unique=True)
    hashed_password = Column(String(20))

    is_admin = Column(Boolean, default=False)
    subjects = relation(
        "Subject", secondary=association_table, back_populates="students"
    )
