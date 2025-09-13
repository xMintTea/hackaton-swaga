from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    Depends,
    status,
    Form
    )
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import hashlib
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.openapi.utils import get_openapi
from jwt import InvalidTokenError

from database import engine, session_local
from schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    CreateDistrict,
    District as DistrictSchema,
    User as UserSchema,
    Response as ResponseSchema,
    Token
)
from auth import utils_jwt


from models import Base, User, District
from static import Roles


app = FastAPI()

#http_bearer = HTTPBearer()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/login/",)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    # и другие адреса, с которых может приходить запрос
]



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


@app.post("/login")
def login(creds: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    query = db.query(User).filter(
        User.login == creds.login,
        User.password == get_hash(creds.password)
    )

    user = query.first()
    if user is not None:

        jwt_payload = {
            "sub": str(user.id),
            "username": user.login,
        }
        
        access_token = utils_jwt.encode_jwt(jwt_payload)
        return Token(access_token=access_token, token_type="bearer")
    
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




def validate_auth_user(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                                 detail="invalid login or password")

    if not (user:= db.query(User).where(User.login == username).filter(User.password == get_hash(password)).first()):
        raise unauthed_exc
    
    return user


@app.post("/login/", response_model=Token)
def auth_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": str(user.id),
        "login": user.login
    }
    
    token = utils_jwt.encode_jwt(jwt_payload)
    
    return Token(access_token=token, token_type="Bearer")


def get_current_token_payload(
    #creds: HTTPAuthorizationCredentials = Depends(http_bearer)
    token: str = Depends(oath2_scheme)
    ) -> dict:
    #token = creds.credentials
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Token Error: {e}")

    return payload
    

def get_current_auth_user(payload: dict = Depends(get_current_token_payload),  db: Session = Depends(get_db)) -> UserSchema:
    user_id: str | None = payload.get("sub")

    if user:=db.query(User).where(User.id == user_id).first():
        return user
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/users/me")
def  auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_auth_user)
):
    iat = payload.get("iat")
    exp = payload.get("exp")
    
    return {
        "id": user.id,
        "login": user.login,
        "password": user.password,
        "ait": iat,
        "exp": exp
    }
