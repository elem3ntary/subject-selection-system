from fastapi import FastAPI
from sqlalchemy.orm.session import Session
from .routers import public, user, admin
from .db.connection import engine, SessionLocal
from .db.base import Base, ConfigValue
from .core.config import db_config
import uvicorn

Base.metadata.create_all(bind=engine)


def setup_db_config():

    db: Session = SessionLocal()
    for key, value in db_config.items():
        prop = db.query(ConfigValue).filter_by(prop=key).one_or_none()
        if not prop:
            config_value = ConfigValue(prop=key, value=value)
            db.add(config_value)

    db.commit()
    db.close()


setup_db_config()

app = FastAPI()
app.include_router(public.router)
app.include_router(user.router)
app.include_router(admin.router)


@app.get("/")
def index():
    return {"message": "Welcome to index page"}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
