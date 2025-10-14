from fastapi import (
    Depends,
    Request,
    APIRouter
)
from sqlalchemy.orm import Session

from templates import templates
from db_helpher import get_db
from helpers import get_leaderboard




router = APIRouter()

@router.get("/", name="index")
def index_page(
    request: Request,
    db: Session = Depends(get_db)
):
    
    leaders = get_leaderboard(db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "leaders": leaders})
 




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



