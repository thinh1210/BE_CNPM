from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.admin import getUser
from app.schemas.user import User_Short
from app.schemas.metadata import Metadata
from app.schemas.admin import getUser,changeUserStatus
from app.schemas.metadata import Metadata
from app.crud.crud_user import get_all_user,change_user_status
from typing import List
from app.api.dependencies import SessionDep,get_current_user,CurrentUser,isAdmin
from sqlmodel import select
from app.model import User


router = APIRouter()

router.include_router(
    router=APIRouter(),
    dependencies=Depends(isAdmin),
)
@router.get("/all_user", response_model=getUser)
def get_all_user_data(session: SessionDep, metadata: Metadata| None):
    '''
    Get all user (username, MSSV, lastname, firstname, email, isActive)
    
    '''
    if (metadata is None):
        metadata = Metadata()
    users, metadata = get_all_user(session, metadata)
    if not users:
        raise HTTPException(status_code=404, detail="No user found")
    users_out= List[User_Short]
    for user in users:
        users_out.append(User_Short(
            username=user.username,
            MSSV=user.MSSV,
            lastname=user.lastname,
            firstname=user.firstname,
            email=user.email,
            isActive=user.isActive
        ))
    return {
        "msg": "Get user successfully",
        "data": users_out,
        "metadata": metadata
    }


@router.put("/change_user_status/{username}", response_model=changeUserStatus)
def admin_change_user_status(username: str, isActive: bool, session: SessionDep):
    '''
    Change user status (isActive)
    
    '''
    user= change_user_status(session, username, isActive)
    if not user:
        raise HTTPException(status_code=404, detail="Have something wrong")
    return{
        "msg": "Change user status successfully",
        "data": User_Short(
            username=user.username,
            MSSV=user.MSSV,
            lastname=user.lastname,
            firstname=user.firstname,
            email=user.email,
            isActive=user.isActive
        )
    }