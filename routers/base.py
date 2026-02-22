from fastapi import (
    Depends,
    Request,
    APIRouter
)
from sqlalchemy.orm import Session

from templates import templates
from utils.db_helpher import get_db
from utils.helpers import get_leaderboard
from models import Course
from static import CourseLvl




router = APIRouter()

@router.get("/", name="index")
def index_page(
    request: Request,
    leaders = Depends(get_leaderboard),
    db: Session = Depends(get_db)
):
    
    beginers_courses = db.query(Course).where(Course.course_lvl == CourseLvl.BEGGINER).limit(3)
    pro_courses = db.query(Course).where(Course.course_lvl == CourseLvl.PRO).limit(3)
    
    
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "leaders": leaders, "beginners_courses" : beginers_courses, "pro_courses" : pro_courses})
 




@router.get("/help", name="help")
def get_help(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={"request": request,})



@router.get("/partners", name="partners")
def partners(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="partners.html",
        context={"request": request,}) 


@router.get("/vacancies", name="vacancies")
def vacancies(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="vacancies.html",
        context={"request": request}) 


@router.get("/team", name="team")
def team(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="team.html",
        context={"request": request,}) 


@router.get("/contacts", name="contacts")
def contanct(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"request": request})



