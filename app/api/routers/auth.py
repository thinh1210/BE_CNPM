from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.user import UserIn, UserOut, Token
from app.crud.crud_user import create_user, authenticate_user
from app.cores.security import create_access_token
from app.api.dependencies import SessionDep,get_current_user,CurrentUser
from sqlmodel import select
from app.model import User
router = APIRouter()



# @router.post("/register", response_model=UserOut)
# def register(user_in: UserCreate, session: SessionDep):
#     existing_user = session.exec(
#         select(User).where(User.email == user_in.email)
#     ).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     user = create_user(session, user_in)
#     return user

# @router.post("/login", response_model=Token)
# def login(email: str, password: str, session: SessionDep):
#     user = authenticate_user(session, email, password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user:CurrentUser ):
    return current_user


@router.post("/login", response_model=Token)
def login(data: UserIn, session: SessionDep):
    user = authenticate_user(session, data.username, data.password)
    if not user:
        user= create_user(session, data)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(
        data={"sub": user.username}
        
        )

    return {"access_token": access_token, "token_type": "bearer"}

