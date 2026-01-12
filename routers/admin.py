from fastapi import (
    Depends,
    Request,
    APIRouter
)
from sqlalchemy.orm import Session, joinedload
from templates import templates

from models import (
    User,
    Title, 
    Achievement,
    Course,
    TestQuestion
    )
from utils.db_helpher import get_db


router = APIRouter(prefix="/admin", tags=["Admins"])

@router.get("/")
def admin_panel(request: Request):
    """Админ-панель с навигацией по разделам управления"""
    return templates.TemplateResponse(
        request=request,
        name="admin_panel.html"
    )
    
    
@router.get("/manage/test/")
def manage_test_questions_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления вопросами теста"""
    questions = db.query(TestQuestion).order_by(TestQuestion.order).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_test.html",
        context={"request": request, "questions": questions}
    )



@router.get("/manage/titles/")
def manage_titles_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления титулами"""
    titles = db.query(Title).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_titles.html",
        context={"request": request, "titles": titles}
    )



    

@router.get("/manage/achievements/")
def manage_achievements_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления ачивками"""
    achievements = db.query(Achievement).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_achievements.html",
        context={"request": request, "achievements": achievements}
    )
    


@router.get("/manage/courses/")
def manage_courses_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления курсами и темами"""
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_courses.html",
        context={"request": request, "courses": courses}
    )




@router.get("/manage/users/")
def manage_users_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления пользователями"""
    users = db.query(User).options(
        joinedload(User.title),
        joinedload(User.achievements),
    ).all()
    titles = db.query(Title).all()
    achievements = db.query(Achievement).all()
    courses = db.query(Course).all()
    
    return templates.TemplateResponse(
        request=request,
        name="manage_users.html",
        context={
            "request": request, 
            "users": users, 
            "titles": titles, 
            "achievements": achievements, 
            "courses": courses
        }
    )

