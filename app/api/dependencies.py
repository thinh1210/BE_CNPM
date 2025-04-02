from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
import jwt
from sqlmodel import Session
from app.cores.db import engine
from app.cores.security import ALGORITHM
from app.cores.config import API_V1_STR,SECRET_KEY
from app.model import User
from app.crud.crud_user import get_user_by_username
from app.cores.security import decode_access_token
# from app.crud.crud_user import get_user_by_email

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/auth/login")
oauth2_scheme = HTTPBearer() 

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]



def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        token_str = token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token
        username=decode_access_token(token_str)
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 1")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 2")
    
    user = get_user_by_username(session, username)
    if not user or not user.isActive:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_user(current_user: User = Depends(get_current_user)) -> bool:
    return current_user.isActive & current_user.isUser

isAcitveUser = Annotated[bool, Depends(get_current_active_user)]

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> bool:
    return current_user.isAdmin

isAdminUser = Annotated[bool, Depends(get_current_admin_user)]
