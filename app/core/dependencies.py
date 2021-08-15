from fastapi import Depends
from ..db.connection import SessionLocal
from .security import oauth2_scheme


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    # process token
    ...
