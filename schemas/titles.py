from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TitleCreate(BaseModel):
    name: str

class TitleResponse(BaseModel):
    id: int
    name: str
    
    model_config = {
        "from_attributes": True
    }
        
