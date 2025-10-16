
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List



class UserAnswerSchema(BaseModel):
    question_id: int
    answer_id: int


class TestSubmissionSchema(BaseModel):
    answers: List[UserAnswerSchema]

class TestRecommendationResponse(BaseModel):
    creative_score: int
    analytical_score: int
    recommended_course: str
    

class TestQuestionCreate(BaseModel):
    text: str
    order: int

class TestQuestionUpdate(BaseModel):
    text: str
    order: int

class TestAnswerCreate(BaseModel):
    question_id: int
    answer_text: str
    creative_value: int
    analytical_value: int

class TestAnswerUpdate(BaseModel):
    answer_text: str
    creative_value: int
    analytical_value: int
    
    
class TestAnswerOptionSchema(BaseModel):
    id: int
    answer_text: str
    creative_value: int
    analytical_value: int

    class Config:
        orm_mode = True

class TestQuestionSchema(BaseModel):
    id: int
    text: str
    order: int
    answer_options: List[TestAnswerOptionSchema]

    class Config:
        orm_mode = True