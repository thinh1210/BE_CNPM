from fastapi import FastAPI
from app.api.routers.auth import router as auth_router
from app.cores.config import DATABASE_URL, API_V1_STR
from sqlmodel import SQLModel

app = FastAPI(title="Auth API")

app.include_router(auth_router, prefix=f"{API_V1_STR}/auth", tags=["auth"])

@app.get("/")
def on_startup():
    return {"message": "Welcome to the Fast API"}