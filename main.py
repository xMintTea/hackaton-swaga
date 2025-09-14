from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    Depends,
    status,
    Form,
    Request
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload
from database import engine
from typing import List
from sqlalchemy.exc import IntegrityError
from templates import templates


from models import (
    Base, 
    User, 
    Student, 
    Title, 
    Achievement,
    Course,
    Topic,
    )
from schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    User as UserSchema,
    Response as ResponseSchema,
    Token,
    StudentRegisterSchema,
    TitleResponse,
    AchievementResponse,
    AchievementCreate,
    SetCourseRequest,
    CourseResponse,
    TopicResponse,
    TopicCreate,
    CourseCreate
)
from helpers import create_access_token, create_refresh_token
from validation import (
    get_current_token_payload,
    get_current_auth_user,
    get_current_auth_user_for_refresh
)
from db_helpher import get_db
from config.settings import settings
from utils.functions import get_hash, get_origins


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





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



@app.get("/users/{login}")
def user_profile(login: str, request: Request, db: Session = Depends(get_db)):
    
    if token:= request.cookies.get("access_token"):
        print(login)
        if user := db.query(User).filter(User.login == login).first():
            return user
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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






# Эндпоинты для курсов
@app.post("/courses", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        description=course.description
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    return courses

@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.topics)).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.title = course.title  # type: ignore
    db_course.description = course.description  # type: ignore
    
    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}


# Эндпоинты для топиков
@app.post("/topics", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли курс
    course = db.query(Course).filter(Course.id == topic.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic = Topic(
        course_id=topic.course_id,
        title=topic.title,
        content=topic.content,
        order=topic.order
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@app.get("/courses/{course_id}/topics", response_model=List[TopicResponse])
def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    topics = db.query(Topic).filter(Topic.course_id == course_id).order_by(Topic.order).all()
    return topics

@app.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@app.put("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Проверяем, существует ли новый курс (если изменился course_id)
    if topic.course_id != db_topic.course_id:
        course = db.query(Course).filter(Course.id == topic.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic.course_id = topic.course_id  # type: ignore
    db_topic.title = topic.title  # type: ignore
    db_topic.content = topic.content  # type: ignore
    db_topic.order = topic.order  # type: ignore
    
    db.commit()
    db.refresh(db_topic)
    return db_topic


@app.delete("/topics/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted successfully"}


# Эндпоинт для установки курса студенту
@app.post("/students/{student_id}/set-course")
def set_student_course(
    student_id: int, 
    request: SetCourseRequest, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    student.current_course_id = request.course_id  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Course set successfully", "student": student}