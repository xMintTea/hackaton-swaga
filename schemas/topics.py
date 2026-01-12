from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from typing import Annotated

class TopicBase(BaseModel):
    name: str
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
    name: str
    content: Optional[str] = None
    order: int

    model_config = ConfigDict(from_attributes=True)