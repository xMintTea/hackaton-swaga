from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from static import Roles

class UserBase(BaseModel):
    nickname: str
    login: str
    password: str
    email: str
    role: Roles = Roles.USER
    

class Response(BaseModel):
    data: str


class UserResponse(BaseModel):
    id: int
    nickname: str
    login: str
    email: str
    role: Roles

    model_config = {
        "from_attributes": True
    }



class User(UserBase):
    id: int

    
    model_config = {
        "from_attributes": True
    }


class StudentResponse(BaseModel):
    id: int
    user: UserResponse

    model_config = {
        "from_attributes": True
    }


class UserRegisterSchema(UserBase):
    pass




class UserLoginSchema(BaseModel):
    login: str
    password: str


class StudentRegisterSchema(BaseModel):
    user_id: int
    

    

    
class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    
    
    
    
    
class AchievementCreate(BaseModel):
    name: str
    description: str

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        orm_mode = True

class TitleCreate(BaseModel):
    name: str

class TitleResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True