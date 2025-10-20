from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

from static import Roles

class UserBase(BaseModel):
    nickname: Annotated[str,
                        Field(...,
                              min_length=2,
                              max_length=20)]
    login:  Annotated[str,
                        Field(...,
                              min_length=2,
                              max_length=20)]
    password:  Annotated[str,
                        Field(...,
                              min_length=2,
                              max_length=20)]
    email: EmailStr
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
