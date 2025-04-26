from pydantic import BaseModel, EmailStr
from typing import Optional

class Register_In(BaseModel):
    username: str 
    password: str 
    lastname: str
    firstname: str
    email: EmailStr


class UserBase(BaseModel):
    username: str 
    password: str 


class UserIn(UserBase):
    pass

class UserOut(UserBase):
    id: int
    username: str
    password: str
    MSSV: int |None
    lastname:str
    firstname:str
    email: EmailStr
    isUser: bool = True
    isAdmin: bool = False
    isActive: bool = True

class User_Short(BaseModel):
    username: str
    MSSV: int |None
    lastname:str
    firstname:str
    email: EmailStr
    isActive: bool = True


class Token(BaseModel):
    access_token: str

class UserOut_json(BaseModel):
    msg: str
    data: UserOut | None = None

class Token_json(BaseModel):
    msg: str
    data: None | dict = None
    access_token: None | str = None

class UpdateUser(BaseModel):
    lastname: str | None = None
    firstname: str | None = None
    email: EmailStr | None = None

class Update_password(BaseModel):
    old_password: str
    new_password: str