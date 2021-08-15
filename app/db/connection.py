from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import SQLALCHEMY_DB_LINK

engine = create_engine(SQLALCHEMY_DB_LINK, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
