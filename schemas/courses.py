from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Annotated

from schemas.topics import TopicResponse

class CourseCreate(BaseModel):
    title: Annotated[
        str,
        Field(...,
              min_length=4,
              max_length=16) #TODO: ЭТО СЛИШКОМ МАЛО, НУЖНО БУДЕТ ПОРЕШАТЬ НА ФРОНТЕ ПРОБЛЕМУ И УДЕЛНИТЬ ЗДЕСЬ
    ]
    description: Annotated[str,
                        Field(max_length=39)]

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    topics: List[TopicResponse] = []

    model_config = {
        "from_attributes": True
    }




class SetCourseRequest(BaseModel):
    course_id: int