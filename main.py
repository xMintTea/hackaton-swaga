from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    Depends,
    status,
    Form,
    Request,

    )
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload
import hashlib
from datetime import datetime
from database import engine
from typing import List
from schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    User as UserSchema,
    Response as ResponseSchema,
    Token,
    StudentRegisterSchema,
    TitleCreate,
    TitleResponse,
    AchievementResponse,
    AchievementCreate
)
from authx import AuthX, AuthXConfig

from sqlalchemy.exc import IntegrityError
from templates import templates, templates_folder

from models import (
    Base, 
    User, 
    Student, 
    Title, 
    Achievement
    )
from helpers import create_access_token, create_refresh_token
from validation import (
    get_current_token_payload,
    get_current_auth_user,
    get_current_auth_user_for_refresh
)
from db_helpher import get_db
from config.settings import settings


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)







def get_hash(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()

    

@app.get("/", name="index")
def index_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="index.html")
 

@app.get("/users/")
def users_page(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"request": request, "users": users})


@app.get("/users/alt")
def users_page_alt(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    
    return users

@app.get("/students/alt")
def students_page_alt(
    db: Session = Depends(get_db)
):
    users = db.query(Student).options(joinedload(Student.user)).all()
    
    return users


@app.post("/students/register")
def students_register(
    student: StudentRegisterSchema,
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter(User.id == student.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db_student = Student(user_id=student.user_id)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        return {"message": "Student registered successfully", "student_id": db_student.id}
    
    except IntegrityError as e:
        db.rollback()
        return {"message": "This user is already a student"}




@app.post("/login")
def login(creds: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    query = db.query(User).filter(
        User.login == creds.login,
        User.password == get_hash(creds.password)
    )

    user = query.first()
    if user is not None:
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        
        print(response.set_cookie("access_token", access_token))
        
        return Token(access_token=access_token,
                     refresh_token=refresh_token,
                     token_type="bearer")
    
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.post("/register/", response_model=ResponseSchema)
def registerUser(user: UserRegisterSchema, db: Session = Depends(get_db)) -> dict:

    db_user = User(
        login=user.login,
        nickname=user.nickname,
        password=get_hash(user.password),
        email=user.email

    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"data":"Пользователь успешно добавлен"}

    except IntegrityError as e:
        db.rollback()
        print(e)
        
        return {"data": "Пользователь с таким логином уже существует"}

    


def validate_auth_user(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                                 detail="invalid login or password")

    if not (user:= db.query(User).where(User.login == username).filter(User.password == get_hash(password)).first()):
        raise unauthed_exc
    
    return user




@app.post("/login/", response_model=Token)
def auth_user(response: Response, user: UserSchema = Depends(validate_auth_user)):

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie("access_token", access_token)
    
    return Token(access_token=access_token, refresh_token=refresh_token)



@app.post("/refresh/", response_model=Token, response_model_exclude_none=True)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return Token(
        access_token=access_token
    )




@app.get("/users/me")
def  auth_user_check_self_info(
    request: Request,
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_auth_user)
):
    token = request.cookies.get("access_token")
    
    print(token)
    
    iat = payload.get("iat")
    exp = payload.get("exp")
    
    return {
        "id": user.id,
        "login": user.login,
        "password": user.password,
        "ait": iat,
        "exp": exp
    }


@app.get("/users/me/alt")
def cookie_login(request: Request):
    

    if token:= request.cookies.get("access_token"):
        return get_current_token_payload(token)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/achievements", response_model=List[AchievementResponse])
def get_all_achievements(db: Session = Depends(get_db)):
    """Получить все ачивки"""
    achievements = db.query(Achievement).all()
    return achievements

@app.post("/achievements", response_model=AchievementResponse)
def create_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db)
):
    """Создать новую ачивку"""
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

# Эндпоинты для титулов
@app.get("/titles", response_model=List[TitleResponse])
def get_all_titles(db: Session = Depends(get_db)):
    """Получить все титулы"""
    titles = db.query(Title).all()
    return titles

@app.post("/titles", response_model=TitleResponse)
def create_title(
    title: TitleCreate,
    db: Session = Depends(get_db)
):
    """Создать новый титул"""
    # Проверяем, существует ли титул с таким именем
    existing_title = db.query(Title).filter(Title.name == title.name).first()
    if existing_title:
        raise HTTPException(status_code=400, detail="Title with this name already exists")
    
    db_title = Title(name=title.name)
    
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    
    return db_title

# Дополнительно: эндпоинт для получения студентов с информацией о пользователях
@app.get("/students/with-users", response_model=List[dict])
def get_students_with_users(db: Session = Depends(get_db)):
    """Получить всех студентов с информацией о пользователях"""
    students = db.query(Student).options(joinedload(Student.user)).all()
    
    result = []
    for student in students:
        result.append({
            "student_id": student.id,
            "xp": student.xp,
            "lvl": student.lvl,
            "currency": student.currency,
            "user": {
                "id": student.user.id,
                "nickname": student.user.nickname,
                "login": student.user.login,
                "email": student.user.email,
                "role": student.user.role.value if student.user.role else None
            }
        })
    
    return result