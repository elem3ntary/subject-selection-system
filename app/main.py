from fastapi import FastAPI
from .routers import public
from .db.connection import engine
from .db.base import Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(public.router)


@app.get("/")
def index():
    return {"message": "Welcome to index page"}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
