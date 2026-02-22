from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

class TitleCreate(BaseModel):
    name: Annotated[
        str,
        Field(...,min_length=1, max_length=124, title="Название титула")
    ]

class TitleResponse(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
        
