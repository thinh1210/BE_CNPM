from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

@app.middleware("http")
async def check_token_middleware(request: Request, call_next):
    # Middleware không thể dùng Depends => tự lấy header
    if request.url.path.startswith("/admin"):
        auth = request.headers.get("Authorization")
        if auth != "Bearer mysecrettoken":
            return JSONResponse(status_code=403, content={"detail": "Permission denied"})
    return await call_next(request)

@app.get("/admin/dashboard", dependencies=[Depends(security)])
def admin_dashboard():
    return {"message": "Bạn đang truy cập trang quản trị"}

@app.get("/public")
def public_page():
    return {"message": "Trang công khai"}
