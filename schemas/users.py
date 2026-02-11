from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional, List

from static import Roles
from schemas.topics import TopicBase

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


class UserRegisterSchema(UserBase):
    pass


class UserLoginSchema(BaseModel):
    login: str
    password: str


class User(UserBase):
    id: int

    
    model_config = ConfigDict(from_attributes=True)


class FrameResponse(BaseModel):
    id: int
    name: str
    img_href: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class TitleResponse(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class AvatarResponse(BaseModel):
    id: int
    name: str
    image_url: str
    is_public: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    about_me: Optional[str] = None
    current_frame: Optional[FrameResponse] = None
    current_title: Optional[TitleResponse] = None
    current_avatar: Optional[AvatarResponse] = None


    available_frames: List[FrameResponse] = []
    available_titles: List[TitleResponse] = []
    available_avatars: List[AvatarResponse] = []
    achievements: List[AchievementResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class GamificationRecordResponse(BaseModel):
    xp: int
    lvl: int
    currency: int
    
    model_config = ConfigDict(from_attributes=True)


class CourseResponse(BaseModel):
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    nickname: str
    login: str
    email: str
    role: Optional[str] = None
    
    profile: Optional[UserProfileResponse] = None
    gamificationRecord: Optional[GamificationRecordResponse] = None
    courses: List[CourseResponse] = []
    completed_topics: List[TopicBase] = []
    
    model_config = ConfigDict(from_attributes=True)