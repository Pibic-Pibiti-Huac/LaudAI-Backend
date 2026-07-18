from fastapi import FastAPI
from app.routers.model_routers import router as model_router

app = FastAPI(
    root_path="/api/v1"
)

@app.get("/")
def hello_world():
    return {
        "message": "hello_world"
    }

app.include_router(model_router)
