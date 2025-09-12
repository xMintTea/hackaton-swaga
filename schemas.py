from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int
    
class Student(UserBase):
    id: int
    
    class Config:
        orm_mode = True