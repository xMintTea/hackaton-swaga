from fastapi import (
    FastAPI,
)   
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload
from database import engine
from typing import List
from sqlalchemy.exc import IntegrityError
from templates import templates
from fastapi.staticfiles import StaticFiles

from routers import achievements
from routers import admin
from routers import auth
from routers import base
from routers import courses
from routers import skilltest
from routers import students
from routers import titles
from routers import topics
from routers import users

from database import Base


from utils.functions import get_origins

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


app.include_router(achievements.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(base.router)
app.include_router(courses.router)
app.include_router(skilltest.router)
app.include_router(students.router)
app.include_router(titles.router)
app.include_router(topics.router)
app.include_router(users.router)