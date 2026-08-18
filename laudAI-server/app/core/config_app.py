from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def include_routers(app: FastAPI):
    from app.routers.model_routers import router as model_router

    app.include_router(model_router)

def config_middleware_cors(app: FastAPI):
    origins = [
        "http://react:8443",
        "http://localhost:8443"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,            
        allow_credentials=True,           
        allow_methods=["*"],           
        allow_headers=["*"]
    )