from fastapi import (
    HTTPException,
    Response,
    Depends,
    APIRouter
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import User, UserProfile, GamificationRecord
from schemas.users import (
    UserLoginSchema,
    UserRegisterSchema,
    User as UserSchema
)

from schemas.other import Response as ResponseSchema, Token
from static import Roles


from utils.helpers import create_access_token, create_refresh_token
from validation import get_current_auth_user_for_refresh
from utils.db_helpher import get_db
from utils.functions import get_hash
from utils.helpers import validate_auth_user


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login/", response_model=Token)
def auth_user(response: Response, user: UserSchema = Depends(validate_auth_user)):

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie("access_token", access_token)
    
    return Token(access_token=access_token, refresh_token=refresh_token)



@router.post("/refresh/", response_model=Token, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return Token(
        access_token=access_token
    )



@router.post("/register/", response_model=ResponseSchema)
def registerUser(user: UserRegisterSchema, db: Session = Depends(get_db)) -> dict:

    user_profile = UserProfile()
    game_record = GamificationRecord()

    db_user = User(
        login=user.login,
        nickname=user.nickname,
        password=get_hash(user.password),
        email=user.email,
        profile=user_profile,
        role=Roles.USER,
        gamerec=game_record
    )
    try:
        db.add(user_profile)
        db.add(game_record)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"data":"Пользователь успешно добавлен"}

    except IntegrityError as e:
        db.rollback()
        
        return {"data": "Пользователь с таким логином уже существует"}

    



@router.post("/login")
def login(creds: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    query = db.query(User).filter(
        User.login == creds.login,
        User.password == get_hash(creds.password)
    )

    user = query.first()
    if user is not None:
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        
        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)
    
        
        return Token(access_token=access_token,
                     refresh_token=refresh_token,
                     token_type="bearer")
    
    raise HTTPException(status_code=401, detail="Incorrect username or password")


