from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from static import Roles


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True)




class StudentCourse(BaseModel):
    __tablename__  = "student_course"
    student_id = Column("student_id", Integer, ForeignKey("users.id"))
    course_id = Column("course_id", Integer, ForeignKey("courses.id"))

class StudentTopics(BaseModel):
    __tablename__ = "student_topic"
    student_id = Column("student_id", Integer, ForeignKey("users.id"))
    topic_id = Column("topic_id", Integer, ForeignKey("topics.id"))

class UserProfile(BaseModel):
    __tablename__ = "users_profiles"
    
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    
    about_me = Column(String)
    

    current_frame_id = Column(Integer)
    available_frames = relationship("Frame")
    
    current_title = Column(Integer)
    available_titles = relationship("Title")
    
    achievements = relationship("Achievement")

    def __repr__(self):
        return f"<UserProfile({self.id=},{self.current_frame_id=}, {self.available_frames=})>"


class GamificationRecord(BaseModel):
    __tablename__ = "game_records"
    
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="gamificationRecord")
    
    xp = Column(Integer, default=0)
    lvl = Column(Integer, default=1)
    currency = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<GameRecord({self.id=}, {self.user_id=}, {self.xp=})>"


class User(BaseModel):
    __tablename__ = "users"
    
    login = Column(String)
    password = Column(String)
    role = Column(Enum(Roles))

    profile = relationship(UserProfile,back_populates="user", uselist=False) # 1 к 1
    gamificationRecord = relationship(GamificationRecord, back_populates="user", uselist=False) # 1 к 1
    courses = relationship("Course", secondary="student_course", back_populates="users")

    completed_topics = relationship("Topic", secondary="student_topic", back_populates="users_completed")

    def __repr__(self):
        return f"<User({self.id=}, {self.login=}, {self.profile=})>"


class Frame(BaseModel):
    __tablename__ = "frames"
    
    name = Column(String)
    img_href = Column(String)
    

    user_id = Column(ForeignKey("users_profiles.id"))
    uploader_id = Column(Integer)

    def __repr__(self):
        return f"<Frame({self.id=}, {self.name=})>"


class Achievement(BaseModel):
    __tablename__ = "achievements"
    
    user_id = Column(ForeignKey("users_profiles.id"))
    
    name = Column(String)
    description = Column(String)


class Title(BaseModel):
    __tablename__ = "titles"

    user_id = Column(ForeignKey("users_profiles.id"))
    
    name = Column(String)


class Course(BaseModel):
    __tablename__ = "courses"
    
    name = Column(String)
    description = Column(String)
    users = relationship(User, secondary="student_course", back_populates="courses")

    topics = relationship("Topic")


    def __repr__(self):
        return f"<Course({self.name=},{self.topics=})>"

class Topic(BaseModel):
    __tablename__ = "topics"
    
    course_id = Column(ForeignKey("courses.id"))
    
    
    name = Column(String)
    content = Column(String)
    order = Column(Integer)
    
    users_completed = relationship(User, secondary="student_topic", back_populates="completed_topics")


    def __repr__(self):
        return f"<Topic({self.name=},{self.users_completed=})>"


class TestQuestion(BaseModel):
    __tablename__ = "test_questions"
    
    text = Column(String)
    order = Column(Integer)
    
    answers = relationship("TestAnswer")

    def __repr__(self):
        return f"<TestQuestion({self.id=}, {self.answers=})>"


class TestAnswer(BaseModel):
    __tablename__ = "test_answers"
    
    question_id = Column(ForeignKey("test_questions.id"))
    text = Column(String)
    analytical_value = Column(Integer)
    creative_value = Column(Integer)


    def __repr__(self):
        return f"<TestAnswer({self.id=})>"


