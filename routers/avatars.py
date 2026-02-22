from fastapi import (
    HTTPException,
    Depends,
    APIRouter,
    Form,
    UploadFile,
    File
)
from sqlalchemy.orm import Session


from models import Avatar

import os
import uuid
from pathlib import Path


from utils.db_helpher import get_db

AVATARS_DIR = Path("web/static/img/avatars")

router = APIRouter(prefix="/avatars", tags=["Avatars"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/")
async def create_avatar(
    name: str = Form(...),
    is_public: bool = Form(True),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):

    if not file.content_type.startswith('image/'): #type: ignore
        raise HTTPException(status_code=400, detail="File must be an image")

    if file.content_type.startswith('image/gif'): #type: ignore
        raise HTTPException(status_code=400, detail="File must be an image")
    
    file_extension = file.filename.split('.')[-1] #type: ignore
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(AVATARS_DIR, filename)
    
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    finally:
        await file.close()
        
    # Создаем URL для доступа к файлу
    image_url = f"/{AVATARS_DIR}/{filename}"
    
    db_avatar = Avatar(
        name=name,
        image_url=image_url,
        is_public=is_public
    )
    
    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)
    
    return db_avatar