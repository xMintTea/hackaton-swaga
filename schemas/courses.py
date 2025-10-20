from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from schemas.topics import TopicResponse

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

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