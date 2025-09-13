from pydantic import BaseModel
from datetime import datetime


from static import Roles


class DistrictBase(BaseModel):
    name: str

class District(DistrictBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class CreateDistrict(DistrictBase):
    pass


class UserBase(BaseModel):
    nickname: str
    login: str
    password: str
    district_id: int
    last_activity_date: datetime
    creation_date: datetime
    role: Roles
    district: District
    

class Response(BaseModel):
    data: str


class User(UserBase):
    id: int

    
    model_config = {
        "from_attributes": True
    }



class UserRegisterSchema(BaseModel):
    nickname: str
    login: str
    password: str
    district_id: int
    role: Roles


class StudentBase(BaseModel):
    id: int
    user_id: int
    total_xp: int
    current_streak: int
    longest_streak: int
    
    user: User


class Student(StudentBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }



class UserLoginSchema(BaseModel):
    login: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str