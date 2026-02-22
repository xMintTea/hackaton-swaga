from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

class AchievementCreate(BaseModel):
    name: Annotated[
        str,
        Field(...,title="Название ачивки",
              min_length=1,
              max_length=17)
    ]
    description: Annotated[
        str,
        Field(...,title="Описание ачивки",
              min_length=1,
              max_length=32)
    ]


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)

