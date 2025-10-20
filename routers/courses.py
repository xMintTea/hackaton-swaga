from fastapi import (
    HTTPException,
    Depends,
    Request,
    APIRouter
)   
from sqlalchemy.orm import Session, joinedload
from typing import List


from templates import templates
from models import Course, Topic
from schemas.courses import CourseResponse, CourseCreate
from schemas.topics import TopicResponse

from utils.db_helpher import get_db



router = APIRouter(prefix="/courses", tags=["Courses"])



@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        description=course.description
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", name="courses")
def get_courses(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    
    # TODO: УБРАТЬ ЭТО
    additional = []
    icons = ["🐍","⚡","☕","🤖","🌐", "🔐"]
    price = [1000, 2500, 3200, 4242, 2222, 2222]
    level = ["Базовый", "Базовый", "Базовый", "Продвинутый", "Продвинутый","Продвинутый"]
    
    for course in courses:
        additional.append({ #type: ignore
                "id" : course.id,
                "title" : course.title,
                "desc" :course.description,
                # "icon" : icons[course.id-1], #type: ignore
                # "price" : price[course.id-1], #type: ignore
                # "lvl" : level[course.id-1], #type: ignore
                "topic_count" : len(course.topics)*3
            }
        )
        
    # additional = list(sorted(additional, key=lambda x: x.get("lvl")))
        
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"request": request, "courses": additional, "additional": additional})



@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int,  request: Request, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.topics)).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    
    response = {
        "title" : course.title,
        "desc" : course.description,
        "studs" : course.students
    }
    
    return templates.TemplateResponse(
        request=request,
        name="cours.html",
        context={"request": request, "course": response})
    



@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}




@router.get("/course/{course_id}", name="course")
def cours(course_id: int,request: Request,db: Session = Depends(get_db)):
    topics = get_course_topics(course_id, db)
    
    
    
    return templates.TemplateResponse(
        request=request,
        name="cours.html",
        context={"request": request,
                 "topics": topics,
                 "cid" : course_id})


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.title = course.title #type: ignore 
    db_course.description = course.description #type: ignore
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}/topics", response_model=List[TopicResponse])
def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    topics = db.query(Topic).filter(Topic.course_id == course_id).order_by(Topic.order).all()
    return topics