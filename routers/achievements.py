from fastapi import (
    HTTPException,
    Depends,
    Request,
    APIRouter
)   
from sqlalchemy.orm import Session, Query
from templates import templates

from models import Achievement
from schemas.achievements import AchievementResponse, AchievementCreate
from utils.db_helpher import get_db



router = APIRouter(prefix="/achievements", tags=["Achievements"])



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
def get_achievements(db: Session = Depends(get_db)):
    return db.query(Achievement).all()


@router.get("/view")
def achievements_view(request: Request, achievements: Query = Depends(get_achievements) ):
    """Страница со всеми ачивками"""

    return templates.TemplateResponse(
        request=request,
        name="achievements.html",
        context={"request": request, "achievements": achievements})




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
