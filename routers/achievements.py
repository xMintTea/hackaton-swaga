from fastapi import APIRouter

router = APIRouter(prefix="/achievements")


from fastapi import (
    HTTPException,
    Depends,
    Request
)   
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload
from database import engine
from typing import List
from sqlalchemy.exc import IntegrityError
from templates import templates
from fastapi.staticfiles import StaticFiles


from models import (
    Achievement,
    )
from schemas import (
    AchievementResponse,
    AchievementCreate
)

from db_helpher import get_db



@router.put("/{achievement_id}", response_model=AchievementResponse)
def update_achievement(achievement_id: int, achievement: AchievementCreate, db: Session = Depends(get_db)):
    db_achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not db_achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    # Проверяем, существует ли другая ачивка с таким именем
    existing_achievement = db.query(Achievement).filter(Achievement.name == achievement.name, Achievement.id != achievement_id).first()
    if existing_achievement:
        raise HTTPException(status_code=400, detail="Achievement with this name already exists")
    
    db_achievement.name = achievement.name # type: ignore
    db_achievement.description = achievement.description # type: ignore
    
    db.commit()
    db.refresh(db_achievement)
    return db_achievement
    
    
@router.delete("/{achievement_id}")
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    db.delete(achievement)
    db.commit()
    return {"message": "Achievement deleted successfully"}


@router.post("/", response_model=AchievementResponse)
def create_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли ачивка с таким именем
    existing_achievement = db.query(Achievement).filter(Achievement.name == achievement.name).first()
    if existing_achievement:
        raise HTTPException(status_code=400, detail="Achievement with this name already exists")
    
    db_achievement = Achievement(
        name=achievement.name,
        description=achievement.description
    )
    
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    
    return db_achievement




@router.get("/")
def get_all_achievements(request: Request,db: Session = Depends(get_db)):
    """Получить все ачивки"""
    achievements = db.query(Achievement).all()
    
        
    return templates.TemplateResponse(
        request=request,
        name="achievements.html",
        context={"request": request, "achievements": achievements})

