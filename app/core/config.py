from os import environ

SQLALCHEMY_DB_LINK = environ.get("SQLALCHEMY_DB_LINK") or "sqlite:///./test.db"

ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)
ACCESS_TOKEN_SECRET = environ.get("ACCESS_TOKEN_SECRET") or "testing purpose"

db_config = {"registration_opened": False}  # initing in main.py
