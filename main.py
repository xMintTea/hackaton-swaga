from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import engine, session_local
#from schemas 
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
        

