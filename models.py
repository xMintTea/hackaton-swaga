from sqlalchemy import Table, Column, Integer, String, DateTime, Enum, ForeignKey, Text, Boolean, func
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
from static import Roles



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Roles), default=Roles.USER)
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=True)
    
    title = relationship("Title", back_populates="users")
    student = relationship("Student", back_populates="user", uselist=False)
    achievements = relationship("Achievement", secondary="user_achievements", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)    
    xp = Column(Integer, default=0)
    lvl = Column(Integer, default=1)
    currency = Column(Integer, default=0)
    current_course_id = Column(Integer, ForeignKey('courses.id')) 
    
    user = relationship("User", back_populates="student")
    current_course = relationship("Course", back_populates="students") 

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    
    users = relationship("User", secondary="user_achievements", back_populates="achievements")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    
    user = relationship("User")
    achievement = relationship("Achievement")

class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    users = relationship("User", back_populates="title")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    user = relationship("User", back_populates="profile")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    topics = relationship("Topic", back_populates="course", order_by="Topic.order")
    students = relationship("Student", back_populates="current_course")  # Обновлено

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    course = relationship("Course", back_populates="topics")


