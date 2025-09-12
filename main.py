from fastapi import FastAPI, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig
import hashlib
from datetime import datetime


from database import engine, session_local
from schemas import UserLoginSchema, UserRegisterSchema, CreateDistrict, District as DistrictSchema, User as UserSchema, Response as ResponseSchema
from models import Base, User, District
from static import Roles


app = FastAPI()
Base.metadata.create_all(bind=engine)


config = AuthXConfig()

#TODO: Опасно, лучше всё это перенести в venv.
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_hash(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


@app.post("/login")
def login(creds: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    
    #TODO: изменить на рабочую реализацию с хэшами и подключением к бд
    
    hashed_password = get_hash(creds.password)
    query = db.query(User).filter(User.login==creds.login and User.password == get_hash(creds.password))
    user = query.first()
    if user is not None:
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token":token}
    
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.post("/register/", response_model=ResponseSchema)
def registerUser(user: UserRegisterSchema, db: Session = Depends(get_db)) -> dict:
    if db.query(User).filter(User.login == user.login).first() is not None:
        raise HTTPException(status_code=400, detail="Этот логин занят")
    

    
    db_user = User(
                   login=user.login,
                   nickname=user.nickname,
                   password=get_hash(user.password),
                   district_id=user.district_id,
                   last_activity_date = datetime.now(),
                   creation_date=datetime.now(),
                   role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"data":"Пользователь успешно добавлен"}


@app.post("/create_dist/", response_model=DistrictSchema)
def createDistrict(district: CreateDistrict, db: Session = Depends(get_db)) -> District:
    db_dist = District(name=district.name)
    db.add(db_dist)
    db.commit()
    db.refresh(db_dist)
    
    return db_dist


# TODO: Тестовая защищённая ручка, убрать после.
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}