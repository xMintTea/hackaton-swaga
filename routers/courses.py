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
        name=course.name,
        description=course.description
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", name="courses")
def get_courses(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    
        
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"request": request})



@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int,  request: Request, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.topics)).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return templates.TemplateResponse(
        request=request,
        name="cours.html",
        context={"request": request, "course": course})
    



@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}



@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.name = course.name # type: ignore
    db_course.description = course.description #type: ignore
    
    db.commit()
    db.refresh(db_course)
    return db_course