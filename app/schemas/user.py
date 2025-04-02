from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str 
    password: str 


class UserIn(UserBase):
    pass

class UserOut(UserBase):
    id: str
    username: str
    password: str
    MSSV: str
    lastname:str
    firstname:str
    email: EmailStr
    isUser: bool = True
    isAdmin: bool = False
    isActive: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"