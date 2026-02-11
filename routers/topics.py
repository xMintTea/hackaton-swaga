from fastapi import (
    HTTPException,
    Depends,
    status,
    Request,
    APIRouter,
)
from sqlalchemy.orm import Session, Query
from templates import templates


from models import Course, Topic, User

from schemas.topics import TopicResponse, TopicCreate, SaveTCompetendTopic
from utils.db_helpher import get_db
from routers.users import get_users
from validation import get_current_token_payload, get_current_auth_user


router = APIRouter(prefix="/topics", tags=["Topics"])


# Эндпоинты для топиков
@router.post("/", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли курс
    course = db.query(Course).filter(Course.id == topic.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic = Topic(
        course_id=topic.course_id,
        name=topic.name,
        content=topic.content,
        order=topic.order
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic



@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int,request: Request, db: Session = Depends(get_db), users: Query = Depends(get_users)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    is_completed = False

    if token := request.cookies.get("access_token"):
        payload = get_current_token_payload(token)
        user: User = get_current_auth_user(payload, users)
        
        if topic in user.completed_topics:
            is_completed = True
    

    return templates.TemplateResponse(
        request=request,
        name="topic.html",
        context={"request": request, "topic": topic, "is_completed": is_completed})


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


@router.post("/complete_topic")
def complete_topic(
    topicToSave: SaveTCompetendTopic,
    db : Session = Depends(get_db),
    users: Query = Depends(get_users)
    ):
    user: User = users.where(User.id == topicToSave.user_id).first() #type: ignore
    topic = db.query(Topic).where(Topic.id == topicToSave.topic_id).first()
    
    if not user:
        raise Exception()
    
    if not topic:
        raise Exception
    
    user.completed_topics.append(topic)
    
    db.commit()
    db.refresh(user)
    return 200
    
    
@router.post("/complete_topic/{topic_id}")
def complete_topic_by_id(
    topic_id: int,
    request: Request,
    db : Session = Depends(get_db),
    users: Query = Depends(get_users)
    ):
    
    if token := request.cookies.get("access_token"):
        payload = get_current_token_payload(token)
        user: User = get_current_auth_user(payload, users)
        
        if not user:
            raise Exception()
    
    
    topic = db.query(Topic).where(Topic.id == topic_id).first()
    

    
    if not topic:
        raise Exception
    
    user.completed_topics.append(topic)
    
    db.commit()
    db.refresh(user)
    return 200
    