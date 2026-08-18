from fastapi import FastAPI
from app.core.config_app import (
    include_routers,
    config_middleware_cors
) 

app = FastAPI(
    root_path="/api/v1"
)

@app.get("/")
def hello_world():
    return {
        "message": "hello_world"
    }

include_routers(app)
config_middleware_cors(app)