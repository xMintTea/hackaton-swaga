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
    

class LevelUpdate(BaseModel):
    level: int

class XPUpdate(BaseModel):
    xp: int

class CurrencyUpdate(BaseModel):
    currency: int


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    topics: List["TopicResponse"] = []

    class Config:
        orm_mode = True
# Pydantic схемы для тем
# Для топиков - сделайте поле order обязательным с значением по умолчанию

class TopicBase(BaseModel):
    title: str
    content: Optional[str] = None
    order: int = Field(default=0, ge=0)


class TopicCreate(TopicBase):
    course_id: int



class TopicUpdate(BaseModel):
    course_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)

class TopicResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str] = None
    order: int 
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SetCourseRequest(BaseModel):
    course_id: int
    
    
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