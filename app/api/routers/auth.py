from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.user import UserIn, UserOut, Token, UserOut_json, Token_json, Register_In
from app.schemas.admin import AdminIn
from app.crud.crud_user import create_user, authenticate_user,register_user
#from app.schemas.metadata import Metadata
from app.api.dependencies import SessionDep,get_current_user,CurrentUser,isUser
from sqlmodel import select
from app.model import User
from app.cores.security import create_access_token, verify_key

router = APIRouter()

# @router.get("/me", response_model=UserOut_json)
# def read_users_me(current_user:CurrentUser ):
#     return{
#         "message": "Get user successfully",
#         "data": current_user
#     }


@router.post("/login", response_model=Token_json)
def login(data: UserIn, session: SessionDep):
    user = authenticate_user(session, data.username, data.password)
    if not user:
        user= create_user(session, data)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        #     return {
        #     "status": 400,
        #     "message": "Your mail or password is incorrect",
        #     "data": None
        # }
    
    access_token = create_access_token (
        data= { "sub": user.username,
                "isuser": user.isUser,
                "isadmin": user.isAdmin,
                "isactive": user.isActive
              }
        )

    return {
        "message": "login successfully",
        "access_token": access_token
    }

@router.post("/register", response_model=UserOut_json)
def register(data: Register_In, session: SessionDep):
    user = authenticate_user(session, data.username, data.password)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
        return {
            "message": "User already exists",
            "data": None
        }
    # db_user = register_user(session, data)
    # if not db_user:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {
        "message": "Register successfully",
        "data": None
    }


@router.post("/register_admin", response_model=UserOut_json)
def register_admin(data: AdminIn , session: SessionDep):
    user = authenticate_user(session, data.username, data.password)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
        # return {
        #     "message": "Username already exists",
        #     "data": None
        # }
    if verify_key(data.key) == False:
        raise HTTPException(status_code=400, detail="Key is incorrect")
        # return {
        #     "message": "Key is incorrect",
        #     "data": None
        # }
    db_user = register_user(session, data, isAdmin=True)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {
        "message": "Register successfully",
        "data": None
    }
