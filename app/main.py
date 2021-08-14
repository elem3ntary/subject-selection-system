from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Welcome to index page"}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
