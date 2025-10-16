

from fastapi import (
    HTTPException,
    Depends,
    APIRouter
)
from sqlalchemy.orm import Session
from typing import List


from models import Title

from schemas.titles import TitleCreate, TitleResponse

from utils.db_helpher import get_db


router = APIRouter(prefix="/titles", tags=["Titles"])

# Эндпоинты для Title
@router.post("/", response_model=TitleResponse)
def create_title(title: TitleCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли титул с таким именем
    existing_title = db.query(Title).filter(Title.name == title.name).first()
    if existing_title:
        raise HTTPException(status_code=400, detail="Title with this name already exists")
    
    db_title = Title(name=title.name)
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title

@router.get("/", response_model=List[TitleResponse])
def get_all_titles(db: Session = Depends(get_db)):
    """Получить все титулы"""
    titles = db.query(Title).all()
    return titles

@router.get("/{title_id}", response_model=TitleResponse)
def get_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title

@router.put("/{title_id}", response_model=TitleResponse)
def update_title(title_id: int, title: TitleCreate, db: Session = Depends(get_db)):
    db_title = db.query(Title).filter(Title.id == title_id).first()
    if not db_title:
        raise HTTPException(status_code=404, detail="Title not found")
    
    # Проверяем, существует ли другой титул с таким именем
    existing_title = db.query(Title).filter(Title.name == title.name, Title.id != title_id).first()
    if existing_title:
        raise HTTPException(status_code=400, detail="Title with this name already exists")
    
    db_title.name = title.name  # type: ignore
    db.commit()
    db.refresh(db_title)
    return db_title

@router.delete("/{title_id}")
def delete_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    
    db.delete(title)
    db.commit()
    return {"message": "Title deleted successfully"}
