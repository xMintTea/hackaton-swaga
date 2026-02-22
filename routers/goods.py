from fastapi import (
    HTTPException,
    Depends,
    Request,
    APIRouter
)   
from sqlalchemy.orm import Session, joinedload
from typing import List


from templates import templates
from models import Goods
from schemas.goods import GoodsCreate, GoodsResponse

from utils.db_helpher import get_db



router = APIRouter(prefix="/goods", tags=["Goods"])


@router.post("/", response_model=GoodsResponse)
def createItem(item: GoodsCreate,db: Session = Depends(get_db)):
    existing_item = db.query(Goods).filter(Goods.name == item.name).first()
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    
    db_item = Goods(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item
    


@router.get("/{item_id}", response_model=GoodsResponse)
def getItem(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Goods).filter(Goods.id == item_id).first()
    
    if item:
        return item
    
    raise HTTPException(status_code=404, detail="No such item exists")