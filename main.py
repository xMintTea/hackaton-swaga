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
from fastapi.staticfiles import StaticFiles


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
    CourseCreate,
    TitleCreate,
    StudentResponse,
    UserResponse,
    LevelUpdate,
    CurrencyUpdate,
    XPUpdate
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
from auth.utils_jwt import decode_jwt

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
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
        
        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)
    
        
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
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    payload = decode_jwt(token=token) #type: ignore
    
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    
    iat = payload.get("iat")
    exp = payload.get("exp")
    
    return {
        "id": user.id, #type: ignore
        "login": user.login, #type: ignore
        "password": user.password, #type: ignore
        "ait": iat,
        "exp": exp
    }


@app.get("/users/manage")
def manage_users_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления пользователями"""
    users = db.query(User).options(
        joinedload(User.title),
        joinedload(User.achievements),
        joinedload(User.student).joinedload(Student.current_course)
    ).all()
    titles = db.query(Title).all()
    achievements = db.query(Achievement).all()
    courses = db.query(Course).all()
    
    return templates.TemplateResponse(
        request=request,
        name="manage_users.html",
        context={
            "request": request, 
            "users": users, 
            "titles": titles, 
            "achievements": achievements, 
            "courses": courses
        }
    )



@app.get("/users/{login}")
def user_profile(login: str, request: Request, db: Session = Depends(get_db)):
    
    if token:= request.cookies.get("access_token"):
        if user := db.query(User).filter(User.login == login).first():
            
            titile = user.title if user.title else "Нет титула"
            
            lvl = user.student.lvl if user.student else 0
            xp = user.student.xp if user.student else 0
            currency = user.student.currency if user.student else 0
            course = user.student.current_course if user.student else None
            
            response = {
                "nickname": user.nickname,
                "title" : titile,
                "role" : user.role,
                "lvl": lvl,
                "xp" : xp,
                "currency": currency,
                "achievements" : user.achievements,
                "course": course
            }
            
            return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"request": request, "user": response})
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)






@app.get("/users/me/alt")
def cookie_login(request: Request):
    if token:= request.cookies.get("access_token"):
        return get_current_token_payload(token)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/achievements")
def get_all_achievements(request: Request,db: Session = Depends(get_db)):
    """Получить все ачивки"""
    achievements = db.query(Achievement).all()
    
        
    return templates.TemplateResponse(
        request=request,
        name="achievements.html",
        context={"request": request, "achievements": achievements})



@app.get("/contacts", name="contacts")
def contanct(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={"request": request})


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



@app.get("/courses/manage")
def manage_courses_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления курсами и темами"""
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_courses.html",
        context={"request": request, "courses": courses}
    )




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

@app.get("/courses", name="courses")
def get_courses(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).options(joinedload(Course.topics)).all()
    
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"request": request, "courses": courses})
    

@app.get("/help", name="help")
def get_help(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={"request": request,})



@app.get("/partners", name="partners")
def partners(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="partners.html",
        context={"request": request,}) 


@app.get("/vacancies", name="vacancies")
def vacancies(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="vacancies.html",
        context={"request": request}) 


@app.get("/team", name="team")
def team(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="team.html",
        context={"request": request,}) 



@app.get("/test", name="test")
def test(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="test.html",
        context={"request": request,}) 



@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int,  request: Request, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.topics)).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    
    response = {
        "title" : course.title,
        "desc" : course.description,
        "studs" : course.students
    }
    
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"request": request, "course": response})
    



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





@app.get("/course/{course_id}", name="course")
def cours(course_id: int,request: Request,db: Session = Depends(get_db)):
    topics = get_course_topics(course_id, db)
    
    
    
    return templates.TemplateResponse(
        request=request,
        name="cours.html",
        context={"request": request,
                 "topics": topics,
                 "cid" : course_id})
    

@app.get("/topic/{topic_id}", name="topic")
def topic(topic_id: int, request: Request, db: Session = Depends(get_db)):
    
    if topic:=db.query(Topic).filter(Topic.id==topic_id).first():
        
        response = {
            "title" : topic.title,
            "content" : topic.content,
            "course_id" : topic.course_id,
            "topic_id" : topic.id
        }
        
        return templates.TemplateResponse(
            request=request,
            name="topic.html",
            context={"request": request, "topic": response})
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)




    
@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.title = course.title #type: ignore 
    db_course.description = course.description #type: ignore
    
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/achievements/manage")
def manage_achievements_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления ачивками"""
    achievements = db.query(Achievement).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_achievements.html",
        context={"request": request, "achievements": achievements}
    )
    
    
@app.put("/achievements/{achievement_id}", response_model=AchievementResponse)
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
    
    
@app.delete("/achievements/{achievement_id}")
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    db.delete(achievement)
    db.commit()
    return {"message": "Achievement deleted successfully"}



@app.get("/titles/manage")
def manage_titles_page(request: Request, db: Session = Depends(get_db)):
    """Страница управления титулами"""
    titles = db.query(Title).all()
    return templates.TemplateResponse(
        request=request,
        name="manage_titles.html",
        context={"request": request, "titles": titles}
    )


# Эндпоинты для Title
@app.post("/titles", response_model=TitleResponse)
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

@app.get("/titles", response_model=List[TitleResponse])
def get_all_titles(db: Session = Depends(get_db)):
    """Получить все титулы"""
    titles = db.query(Title).all()
    return titles

@app.get("/titles/{title_id}", response_model=TitleResponse)
def get_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title

@app.put("/titles/{title_id}", response_model=TitleResponse)
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

@app.delete("/titles/{title_id}")
def delete_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    
    db.delete(title)
    db.commit()
    return {"message": "Title deleted successfully"}

# Эндпоинт для назначения титула пользователю
@app.post("/users/{user_id}/set-title/{title_id}")
def set_user_title(user_id: int, title_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    
    user.title_id = title_id  # type: ignore
    db.commit()
    db.refresh(user)
    
    return {"message": "Title set successfully", "user": user}



# Эндпоинты для управления ачивками пользователей
@app.post("/users/{user_id}/achievements/{achievement_id}")
def add_achievement_to_user(user_id: int, achievement_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    # Проверяем, есть ли уже эта ачивка у пользователя
    if achievement in user.achievements:
        raise HTTPException(status_code=400, detail="User already has this achievement")
    
    user.achievements.append(achievement)
    db.commit()
    db.refresh(user)
    
    return {"message": "Achievement added to user successfully"}

@app.delete("/users/{user_id}/achievements/{achievement_id}")
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

@app.get("/users/{user_id}/achievements", response_model=List[AchievementResponse])
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.achievements


# Эндпоинты для управления студентами
@app.get("/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).options(joinedload(Student.user)).all()
    return students

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.user)).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}/xp")
def update_student_xp(
    student_id: int, 
    xp_data: XPUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp = xp_data.xp #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student XP updated successfully", "student": student}

@app.put("/students/{student_id}/level")
def update_student_level(
    student_id: int, 
    level_data: LevelUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl = level_data.level #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student level updated successfully", "student": student}



@app.get("/admin")
def admin_panel(request: Request):
    """Админ-панель с навигацией по разделам управления"""
    return templates.TemplateResponse(
        request=request,
        name="admin_panel.html"
    )


@app.put("/students/{student_id}/currency")
def update_student_currency(
    student_id: int, 
    currency_data: CurrencyUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency = currency_data.currency #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student currency updated successfully", "student": student}


# Эндпоинты для управления пользователями
@app.put("/users/{user_id}", response_model=UserResponse)
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

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Удаляем связанные записи (студента, если есть)
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if student:
        db.delete(student)
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# Эндпоинты для управления опытом, уровнем и валютой студентов
@app.post("/students/{student_id}/add-xp/{xp_amount}")
def add_student_xp(student_id: int, xp_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp += xp_amount  # type: ignore
    
    # Автоматическое повышение уровня (например, каждые 100 опыта)
    if student.xp >= student.lvl * 100:  # type: ignore
        student.lvl += 1  # type: ignore
    
    db.commit()
    db.refresh(student)
    
    return {"message": f"Added {xp_amount} XP to student", "student": student}

@app.post("/students/{student_id}/remove-xp/{xp_amount}")
def remove_student_xp(student_id: int, xp_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp = max(0, student.xp - xp_amount)  # type: ignore
    
    # Автоматическое понижение уровня (если опыт меньше необходимого для текущего уровня)
    if student.xp < (student.lvl - 1) * 100:  # type: ignore
        student.lvl = max(1, student.lvl - 1)  # type: ignore
    
    db.commit()
    db.refresh(student)
    
    return {"message": f"Removed {xp_amount} XP from student", "student": student}

@app.post("/students/{student_id}/add-currency/{currency_amount}")
def add_student_currency(student_id: int, currency_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency += currency_amount  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": f"Added {currency_amount} currency to student", "student": student}

@app.post("/students/{student_id}/remove-currency/{currency_amount}")
def remove_student_currency(student_id: int, currency_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency = max(0, student.currency - currency_amount)  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": f"Removed {currency_amount} currency from student", "student": student}

@app.post("/students/{student_id}/level-up")
def level_up_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl += 1  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student leveled up", "student": student}

@app.post("/students/{student_id}/level-down")
def level_down_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl = max(1, student.lvl - 1)  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student leveled down", "student": student}

# Эндпоинт для получения валюты по user_id
@app.get("/students/user/{user_id}/currency")
def get_student_currency_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"currency": 0}
    
    return {"currency": student.currency}

# Эндпоинт для получения полной информации о студенте по user_id
@app.get("/students/user/{user_id}")
def get_student_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.user)).filter(Student.user_id == user_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

# Эндпоинт для получения опыта по user_id
@app.get("/students/user/{user_id}/xp")
def get_student_xp_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"xp": 0}
    
    return {"xp": student.xp}

# Эндпоинт для получения уровня по user_id
@app.get("/students/user/{user_id}/level")
def get_student_level_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"level": 0}
    
    return {"level": student.lvl}

