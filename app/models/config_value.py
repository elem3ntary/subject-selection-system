from ..db.connection import Base
from sqlalchemy import Column, Boolean, String, Integer


class ConfigValue(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    prop = Column(String(50), unique=True)
    value = Column(String(50))
