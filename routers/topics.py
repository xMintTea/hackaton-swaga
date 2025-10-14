from fastapi import (
    HTTPException,
    Depends,
    status,
    Request,
    APIRouter
)
from sqlalchemy.orm import Session
from templates import templates


from models import (
    Course,
    Topic
    )
from schemas import (
    TopicResponse,
    TopicCreate
)
from db_helpher import get_db


router = APIRouter(prefix="/topics")


# Эндпоинты для топиков
@router.post("/", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли курс
    course = db.query(Course).filter(Course.id == topic.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic = Topic(
        course_id=topic.course_id,
        title=topic.title,
        content=topic.content,
        order=topic.order
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic



@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Проверяем, существует ли новый курс (если изменился course_id)
    if topic.course_id != db_topic.course_id:
        course = db.query(Course).filter(Course.id == topic.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic.course_id = topic.course_id  # type: ignore
    db_topic.title = topic.title  # type: ignore
    db_topic.content = topic.content  # type: ignore
    db_topic.order = topic.order  # type: ignore
    
    db.commit()
    db.refresh(db_topic)
    return db_topic


@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted successfully"}





@router.get("/{topic_id}", name="topic")
def topic(topic_id: int, request: Request, db: Session = Depends(get_db)):
    
    if topic:=db.query(Topic).filter(Topic.id==topic_id).first():
        
        response = {
            "title" : topic.title,
            "content" : topic.content,
            "course_id" : topic.course_id,
            "topic_id" : topic.id
        }
        
        return templates.TemplateResponse(
            request=request,
            name="topic.html",
            context={"request": request, "topic": response})
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

