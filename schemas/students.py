from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


from schemas.users import UserResponse

class StudentResponse(BaseModel):
    id: int
    user: UserResponse

    model_config = {
        "from_attributes": True
    }
    
class StudentRegisterSchema(BaseModel):
    user_id: int