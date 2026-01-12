from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Boolean
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

class UserAvailableFrames(BaseModel):
    __tablename__ = "user_available_frames"
    user_profile_id = Column("user_id", Integer, ForeignKey("users_profiles.id"))
    frame_id = Column("frame_id", Integer, ForeignKey("frames.id"))

class UserAvailableTitles(BaseModel):
    __tablename__ = "user_available_titles"
    user_profile_id = Column("user_id", Integer, ForeignKey("users_profiles.id"))
    title_id = Column("title_id", Integer, ForeignKey("titles.id"))


class UserAvailableAvatars(BaseModel):
    __tablename__ = "user_available_avatars"
    user_profile_id = Column("user_profile_id", Integer, ForeignKey("users_profiles.id"))
    avatar_id = Column("avatar_id", Integer, ForeignKey("avatars.id"))


class UserPurchases(BaseModel):
    __tablename__ = "user_purchases"
    user_id = Column("user_id", Integer, ForeignKey("users_profiles.id"))
    item_id = Column("item_id", Integer, ForeignKey("goods.id")) 


class UserProfile(BaseModel):
    __tablename__ = "users_profiles"
    
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    
    about_me = Column(String)
    

    current_frame_id = Column(ForeignKey("frames.id"))
    current_frame = relationship("Frame", foreign_keys=[current_frame_id], back_populates="users_with_active_frame")
    available_frames = relationship("Frame", secondary="user_available_frames", back_populates="users_with_frame")

    current_title_id = Column(ForeignKey("titles.id"))
    current_title = relationship("Title", foreign_keys=[current_title_id], back_populates="users_with_active_title")
    available_titles = relationship("Title", secondary="user_available_titles", back_populates="users_with_frame")
    
    current_avatar_id = Column(ForeignKey("avatars.id"))
    current_avatar = relationship(
        "Avatar", 
        foreign_keys=[current_avatar_id],
        back_populates="users_with_active_avatar"
    )
    
    available_avatars = relationship(
        "Avatar", 
        secondary="user_available_avatars",
        back_populates="users_with_avatar"
    )
    
    achievements = relationship("Achievement")
    
    purchases = relationship("Goods", secondary="user_purchases", back_populates="users")
    
    

    def __repr__(self):
        return f"<UserProfile({self.id=},{self.current_frame_id=}, {self.available_frames=})>"


class GamificationRecord(BaseModel):
    __tablename__ = "game_records"
    
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="gamerec")
    
    xp = Column(Integer, default=0)
    lvl = Column(Integer, default=1)
    currency = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<GameRecord({self.id=}, {self.user_id=}, {self.xp=})>"


class User(BaseModel):
    __tablename__ = "users"
    
    login = Column(String)
    nickname = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(Enum(Roles))

    profile = relationship(UserProfile,back_populates="user", uselist=False) # 1 к 1
    gamerec = relationship(GamificationRecord, back_populates="user", uselist=False) # 1 к 1
    courses = relationship("Course", secondary="student_course", back_populates="users")

    completed_topics = relationship("Topic", secondary="student_topic", back_populates="users_completed")

    def __repr__(self):
        return f"<User({self.id=}, {self.login=}, {self.profile=})>"


class Frame(BaseModel):
    __tablename__ = "frames"
    
    name = Column(String)
    img_href = Column(String)
    

    users_with_frame = relationship(UserProfile, secondary="user_available_frames", back_populates="available_frames")
    users_with_active_frame = relationship(UserProfile, foreign_keys="[UserProfile.current_frame_id]", back_populates="current_frame")

    def __repr__(self):
        return f"<Frame({self.id=}, {self.name=})>"


class Achievement(BaseModel):
    __tablename__ = "achievements"
    
    user_id = Column(ForeignKey("users_profiles.id"))
    
    name = Column(String)
    description = Column(String)


class Title(BaseModel):
    __tablename__ = "titles"

    users_with_active_title = relationship(UserProfile, foreign_keys="[UserProfile.current_title_id]", back_populates="current_title")
    users_with_frame = relationship(UserProfile, secondary="user_available_titles", back_populates="available_titles")
    
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
    content = Column(String, nullable=True)
    order = Column(Integer, default=0)
    
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


class Avatar(BaseModel):
    __tablename__ = "avatars"
    
    name = Column(String)
    image_url = Column(String)
    is_public = Column(Boolean, default=True)
    
    users_with_active_avatar = relationship(
        "UserProfile", 
        foreign_keys="[UserProfile.current_avatar_id]",
        back_populates="current_avatar"
    )
    
    users_with_avatar = relationship(
        "UserProfile", 
        secondary="user_available_avatars",
        back_populates="available_avatars"
    )

    def __repr__(self):
        return f"<Avatar({self.id=}, {self.name=})>"
    
    
class Goods(BaseModel):
    __tablename__ = "goods"
    
    name = Column(String)
    
    users = relationship(UserProfile, secondary="user_purchases", back_populates="purchases")