from fastapi import FastAPI, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig

from database import engine, session_local
from schemas import UserLoginSchema 
from models import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)


config = AuthXConfig()
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
        
        
@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    
    #TODO: изменить на рабочую реализацию с хэшами и подключением к бд
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token":token}
    
    raise HTTPException(status_code=401, detail="Incorrect username or password")



# TODO: Тестовая защищённая ручка, убрать после.
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}