from fastapi import (
    HTTPException,
    Depends,
    Request,
    APIRouter
)   
from sqlalchemy.orm import Session, joinedload, Query
from typing import List


from templates import templates
from models import Course, Topic, User
from schemas.courses import CourseResponse, CourseCreate
from routers.users import get_users
from schemas.topics import TopicResponse
from validation import get_current_auth_user, get_current_token_payload

from utils.db_helpher import get_db



router = APIRouter(prefix="/courses", tags=["Courses"])



@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        name=course.name,
        description=course.description,
        price=course.price,
        course_lvl=course.course_lvl
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course



def get_courses_query(db: Session = Depends(get_db)) -> Query:
    return db.query(Course).options(joinedload(Course.topics))



@router.get("/buy/{course_id}", name="buy_course")
def buy_courses(course_id: int, request: Request, courses: Query = Depends(get_courses_query)):
    
    
    course = courses.where(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404)
    
    
    
    return templates.TemplateResponse(
        request=request,
        name="buy_courses.html",
        context={"request": request, "course": course})


@router.get("/", name="courses")
def get_courses(request: Request, users: Query = Depends(get_users), courses: Query = Depends(get_courses_query) ):
    
    available_courses = []
    
    if token:= request.cookies.get("access_token"):
        payload = get_current_token_payload(token)
        user: User = get_current_auth_user(payload, users)
        available_courses.extend(user.courses)
    
     
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"request": request, "courses":courses.all(), "available_courses":available_courses})



@router.get("/{course_id}", response_model=CourseResponse, name="course")
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



@router.post("/grant_course/{course_id}")
def grant_course(course_id: int,  request: Request,db: Session = Depends(get_db), users: Query = Depends(get_users)):
    if token:= request.cookies.get("access_token"):
        payload = get_current_token_payload(token)
        user: User = get_current_auth_user(payload, users)
        
        course: Course = db.query(Course).where(Course.id == course_id).first()
    
        if not course:
            raise HTTPException(status_code=404)
        
        user.courses.append(course)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print(f"Пользователь {user.nickname} получил курс с {course.name}")
        
        