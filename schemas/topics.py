from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import Annotated

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

    model_config = {
        "from_attributes": True
    }