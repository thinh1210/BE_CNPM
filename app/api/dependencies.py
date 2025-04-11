from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlmodel import Session
from app.cores.db import engine
from app.cores.security import ALGORITHM, decode_access_token
from app.cores.config import API_V1_STR, SECRET_KEY
from app.model import User
from app.crud.crud_user import get_user_by_username


# Khai báo HTTPBearer
oauth2_scheme = HTTPBearer()

# Dependency cho database session
def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]

# Lấy thông tin user từ token
def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        token_str = token.credentials
        data = decode_access_token(token_str)
        username = data.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_username(session, username)
    if not user or not user.isActive:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# Kiểm tra vai trò user dựa trên CurrentUser
def check_user_role(token: str) -> bool:
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        # token_str = token.credentials
        data = decode_access_token(token)
        username = data.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return data.get("isuser", False)

isUser = Annotated[bool, Depends(check_user_role)]

# Kiểm tra vai trò admin dựa trên CurrentUser
def check_admin_role(token: str) -> bool:
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        # token_str = token.credentials
        data = decode_access_token(token)
        username = data.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return data.get("isadmin", False)

isAdmin = Annotated[bool, Depends(check_admin_role)]

# Kiểm tra user active dựa trên CurrentUser
def check_active_user(token: str) -> bool:
    try:
        if not str:
            raise HTTPException(status_code=401, detail="Missing token")
        #token_str = str.credentials
        data = decode_access_token(token)
        username = data.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return data.get("isactive", False) & data.get("isuser", False) 

is_activeuser = Annotated[bool, Depends(check_active_user)]