from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Annotated
from static import CourseLvl

from schemas.topics import TopicResponse

class CourseCreate(BaseModel):
    name: Annotated[
        str,
        Field(...,
              min_length=4,
              max_length=16) #TODO: ЭТО СЛИШКОМ МАЛО, НУЖНО БУДЕТ ПОРЕШАТЬ НА ФРОНТЕ ПРОБЛЕМУ И УДЕЛНИТЬ ЗДЕСЬ
    ]
    description: Annotated[str,
                        Field(max_length=39)]
    price: Annotated[float, Field(...)]
    course_lvl: Annotated[CourseLvl, Field(...)]

class CourseResponse(BaseModel):
    id: int
    name: str
    price: float
    course_lvl: CourseLvl
    description: Optional[str] = None
    topics: List[TopicResponse] = []

    model_config = ConfigDict(from_attributes=True)


class SetCourseRequest(BaseModel):
    course_id: int