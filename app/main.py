from fastapi import FastAPI, Depends
from app.api.routers.auth import router as auth_router
from app.api.routers.admin import router as admin_router
from app.api.routers.user import router as user_router
from app.api.dependencies import get_current_active_user, get_current_admin_user
from app.cores.config import DATABASE_URL, API_V1_STR
from sqlmodel import SQLModel

app = FastAPI(title="CNPM API", dependencies=[])

app.include_router(auth_router, 
                   prefix=f"{API_V1_STR}/auth",

                   tags=["auth"])
app.include_router(admin_router, prefix=f"{API_V1_STR}/admin",tags=["admin"])
app.include_router(user_router, prefix=f"{API_V1_STR}/user",tags=["user"])
@app.get("/")
def on_startup():
    return {"message": "Welcome to the Fast API"}