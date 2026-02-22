from fastapi import (
    HTTPException,
    Depends,
    status,
    Request,
    APIRouter,
    Body
)
from sqlalchemy.orm import Session, joinedload, Query
from typing import List
from templates import templates


from models import (
    User, 
    Title, 
    Achievement,
    UserProfile,
    Avatar
    )

from schemas.users import UserRegisterSchema, UserResponse
from schemas.achievements import AchievementResponse

from utils.db_helpher import get_db
from utils.functions import get_hash



router = APIRouter(prefix="/users", tags=["Users"])

def get_users(db: Session = Depends(get_db)) -> Query:
    users = db.query(User).options(
        joinedload(User.profile).joinedload(UserProfile.available_frames),
        joinedload(User.profile).joinedload(UserProfile.current_frame),
        joinedload(User.profile).joinedload(UserProfile.available_titles),
        joinedload(User.profile).joinedload(UserProfile.current_title),
        joinedload(User.profile).joinedload(UserProfile.achievements),
        joinedload(User.profile).joinedload(UserProfile.available_avatars),
        joinedload(User.profile).joinedload(UserProfile.current_avatar),
        joinedload(User.gamerec),
        joinedload(User.courses),
        joinedload(User.completed_topics)
    )
    
    
    return users

@router.get("/", response_model=List[UserResponse])
def users_page(
    request: Request,
    users: Query = Depends(get_users)
):
    
    #return users
    
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"request": request, "users": users.all()})




@router.get("/{login}", name="user_profile")
def user_profile(login: str, request: Request, users: Query = Depends(get_users)):
    if user := users.filter(User.login == login).first():
        title = user.profile.current_title
        lvl = user.gamerec.lvl if user.gamerec else 0
        xp = user.gamerec.xp if user.gamerec else 0
        currency = user.gamerec.currency if user.gamerec else 0
        
        # Получаем текущий аватар
        current_avatar = user.profile.current_avatar
        avatar_url = current_avatar.image_url[4:] if current_avatar else "/static/img/avatars/avatar1.jpg"
        
        print(avatar_url)
        
        # Получаем доступные аватары пользователя
        available_avatars = user.profile.available_avatars
        
        response = {
            "id": user.id,  # Добавляем ID пользователя
            "nickname": user.nickname,
            "title": title,
            "role": user.role,
            "lvl": lvl,
            "xp": xp,
            "currency": currency,
            "achievements": user.profile.achievements,
            "avatar_url": avatar_url,
            "available_avatars": available_avatars
        }
        
        return templates.TemplateResponse(
            request=request,
            name="profile.html",
            context={"request": request, "user": response})
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/{user_id}/set-title/{title_id}")
def set_user_title(user_id: int,
                   title_id: int,
                   users: Query = Depends(get_users),
                   db: Session = Depends(get_db)):
    user = users.filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    title = db.query(Title).filter(Title.id == title_id).first()
    
    if title not in user.profile.available_titles:
        raise HTTPException(status_code=404, detail="User doesn't have that title")

    user.profile.current_title = title
    db.commit()
    db.refresh(user)
    
    return {"message": "Title set successfully", "user": user}


@router.post("/{user_id}/grant-title/{title_id}")
def grant_user_title(user_id: int,
                   title_id: int,
                   users: Query = Depends(get_users),
                   db: Session = Depends(get_db)):
    user = users.filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    title = db.query(Title).filter(Title.id == title_id).first()
    
    if not title:
        return {"message": "No such title"}
    
    user.profile.available_titles.append(title)
    db.commit()
    db.refresh(user)
    
    return {"message": "Title granted successfully", "user": user}


@router.post("/{user_id}/achievements/{achievement_id}")
def add_achievement_to_user(user_id: int, achievement_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    

    if achievement in user.profile.achievements:
        raise HTTPException(status_code=400, detail="User already has this achievement")
    
    user.profile.achievements.append(achievement)
    db.commit()
    db.refresh(user)
    
    return {"message": "Achievement added to user successfully"}


@router.delete("/{user_id}/achievements/{achievement_id}")
def remove_achievement_from_user(user_id: int, achievement_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    # Проверяем, есть ли эта ачивка у пользователя
    if achievement not in user.achievements:
        raise HTTPException(status_code=400, detail="User doesn't have this achievement")
    
    user.achievements.remove(achievement)
    db.commit()
    db.refresh(user)
    
    return {"message": "Achievement removed from user successfully"}


@router.get("/{user_id}/achievements", response_model=List[AchievementResponse])
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.achievements


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, не занят ли новый логин другим пользователем
    if user_data.login != db_user.login:
        existing_user = db.query(User).filter(User.login == user_data.login).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already taken")
    
    # Проверяем, не занят ли новый email другим пользователем
    if user_data.email != db_user.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already taken")
    
    db_user.nickname = user_data.nickname  # type: ignore
    db_user.login = user_data.login  # type: ignore
    db_user.email = user_data.email  # type: ignore
    db_user.password = get_hash(user_data.password)  # type: ignore
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}



@router.get("/{user_id}/avatars")
def get_user_avatars(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(
        joinedload(User.profile).joinedload(UserProfile.available_avatars),
        joinedload(User.profile).joinedload(UserProfile.current_avatar)
    ).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "current_avatar": user.profile.current_avatar,
        "available_avatars": user.profile.available_avatars
    }

# Новый эндпоинт для изменения аватара
@router.post("/{user_id}/avatar")
def change_user_avatar(
    user_id: int,
    avatar_id: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    user = db.query(User).options(
        joinedload(User.profile)
    ).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, есть ли аватар в доступных у пользователя
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Проверяем, доступен ли аватар пользователю (публичный или куплен)
    if not avatar.is_public and avatar not in user.profile.available_avatars:
        raise HTTPException(status_code=403, detail="Avatar not available for this user")
    
    # Устанавливаем новый аватар
    user.profile.current_avatar = avatar
    db.commit()
    db.refresh(user)
    
    return {"message": "Avatar changed successfully", "avatar_url": avatar.image_url}