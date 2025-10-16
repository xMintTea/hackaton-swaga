from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from static import Roles

class UserBase(BaseModel):
    nickname: str
    login: str
    password: str
    email: str
    role: Roles = Roles.USER


class UserResponse(BaseModel):
    id: int
    nickname: str
    login: str
    email: str
    role: Roles

    model_config = {
        "from_attributes": True
    }

class UserRegisterSchema(UserBase):
    pass


class UserLoginSchema(BaseModel):
    login: str
    password: str


class User(UserBase):
    id: int

    
    model_config = {
        "from_attributes": True
    }
