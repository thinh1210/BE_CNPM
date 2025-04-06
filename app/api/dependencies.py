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
    # print(f"Token:{token}")
    try:
        token_str = token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token
        # print(f"Token string:{token_str}")
        data=decode_access_token(token_str)
        username= data["sub"]
        # print(f"Username:{username}")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 1")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 2")
    
    user = get_user_by_username(session, username)

    # print(f"User:{user}")
    if not user or not user.isActive:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user(session: SessionDep, token: TokenDep) -> bool:
    try:
        token_str = token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token
        # print(f"Token string:{token_str}")
        data=decode_access_token(token_str)
        isuser= data["isuser"]
        if isuser is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 1")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 2")
    
    return isuser
    

isUser = Annotated[bool, Depends(get_current_user)]

def get_current_admin_user(session: SessionDep, token: TokenDep) -> bool:
    try:
        token_str = token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token
        # print(f"Token string:{token_str}")
        data=decode_access_token(token_str)
        # username= data["sub"]
        # isuser= data["isuser"]
        isadmin= data["isadmin"]
        if isadmin is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 1")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 2")
    
    return isadmin

isAdmin = Annotated[bool, Depends(get_current_admin_user)]

def get_current_active_user(session: SessionDep, token: TokenDep) -> bool:
    try:
        token_str = token.credentials if isinstance(token, HTTPAuthorizationCredentials) else token
        # print(f"Token string:{token_str}")
        data=decode_access_token(token_str)
        # username= data["sub"]
        isuser= data["isuser"]
        # isadmin= data["isadmin"]
        isactive= data["isactive"]
        # print(f"Username:{username}")

        if isuser is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 1")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token 2")
    
    return isuser&isactive
is_activeuser = Annotated[bool, Depends(get_current_active_user)]