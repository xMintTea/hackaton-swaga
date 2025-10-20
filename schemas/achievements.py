from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class AchievementCreate(BaseModel):
    name: str
    description: str

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    
    model_config = {
        "from_attributes": True
    }

