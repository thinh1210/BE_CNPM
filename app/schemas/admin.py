from pydantic import BaseModel, EmailStr
from app.schemas.user import Register_In, User_Short
from typing import Optional,List
from app.schemas.metadata import Metadata
class AdminIn(Register_In):
    key: None |str= None

class getUser(BaseModel):
    msg: str
    data: List[User_Short] | None = None
    metadata: Metadata | None = None

class changeUserStatus(BaseModel):
    msg: str
    data: None | User_Short = None