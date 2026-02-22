from schemas.users import User as UserSchema
from auth import utils_jwt
from config.settings import settings
from datetime import timedelta


from fastapi import Form, HTTPException, status, Depends
from models import User

from sqlalchemy.orm import Session, joinedload

from utils.functions import get_hash
from utils.db_helpher import get_db


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh" #8RESRESH


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
    ) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD : token_type}
    jwt_payload.update(token_data)
    
    return utils_jwt.encode_jwt(payload=jwt_payload,
                                expire_minutes=expire_minutes,
                                expire_timedelta=expire_timedelta)

def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "login": user.login
    }
    
    return create_jwt(token_type=ACCESS_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_minutes=settings.auth_jwt.access_token_expire_minutes)

def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "login": user.login
    }
    
    return create_jwt(token_type=REFRESH_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days))
    
    

def validate_auth_user(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                                 detail="invalid login or password")

    if not (user:= db.query(User).where(User.login == username).filter(User.password == get_hash(password)).first()):
        raise unauthed_exc
    
    return user

import random

# TODO: Модели поменяли - это наеблнулось
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    leaderboard_list = []
    for user in users:
        total_xp = user.gamerec.lvl * 100 + user.gamerec.xp
        points = round(total_xp / 2.5) 
        leaderboard_list.append((user.nickname, points))
    
    leaderboard_list.sort(key=lambda x: x[1], reverse=True)
    
    result = []
    for position, (nickname, points) in enumerate(leaderboard_list, 1):
        if position > 5:
            break
        
        result.append({
            "position": position,
            "nickname": nickname,
            "points": points
        })
    
    return result
