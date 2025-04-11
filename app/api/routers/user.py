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
# router.include_router(
#     router=APIRouter(),
#     dependencies=Depends(isUser),
# )

@router.get("/me", response_model=UserOut_json)
def read_users_me(current_user:CurrentUser ):
    return{
        "message": "Get user successfully",
        "data": current_user
    }
