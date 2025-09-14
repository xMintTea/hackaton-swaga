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
    current_course_id = Column(Integer, ForeignKey('courses.id'))  # ДОБАВЛЕНО
    
    user = relationship("User", back_populates="student")
    current_course = relationship("Course", back_populates="students")  # Обновлено

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











##################

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     nickname = Column(String)
#     login = Column(String, unique=True, index=True)
#     password = Column(String)
#     email = Column(String, unique=True, index=True)
#     role = Column(Enum(Roles), default=Roles.USER)
#     title_id = Column(Integer, ForeignKey("titles.id"), nullable=True)
    
#     # Relationships
#     title = relationship("Title", back_populates="users")
#     student = relationship("Student", back_populates="user", uselist=False)
#     achievements = relationship("Achievement", secondary="user_achievements", back_populates="users")
#     profile = relationship("UserProfile", back_populates="user", uselist=False)



# class Student(Base):
#     __tablename__ = "students"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), unique=True)    
#     xp = Column(Integer, default=0)
#     lvl = Column(Integer, default=1)
#     currency = Column(Integer, default=0)
    
#     # Relationships
#     user = relationship("User", back_populates="student")


# class Achievement(Base):
#     __tablename__ = "achievements"  # Исправлено написание
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String)
    
#     # Relationships
#     users = relationship("User", secondary="user_achievements", back_populates="achievements")



# class UserAchievement(Base):
#     __tablename__ = "user_achievements"  # Исправлено написание
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     achievement_id = Column(Integer, ForeignKey('achievements.id'))
    
#     # Relationships (опционально)
#     user = relationship("User")
#     achievement = relationship("Achievement")

# class Title(Base):
#     __tablename__ = "titles"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
    
#     # Relationships
#     users = relationship("User", back_populates="title")


# class UserProfile(Base):
#     __tablename__ = "user_profiles"  # Исправлено имя таблицы
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), unique=True)
#     # Добавьте другие поля профиля по необходимости
    
#     # Relationships
#     user = relationship("User", back_populates="profile")

##################


# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     nickname = Column(String)
#     login = Column(String,index=True)
#     password = Column(String)
#     last_activity_date = Column(DateTime)
#     creation_date = Column(DateTime)
#     role = Column(Enum(Roles))
#     title_id = Column(Integer, ForeignKey('titles.id'), nullable=True)
    

#     can_upload_avatar = Column(Boolean, default=False, nullable=False)
#     avatar_id = Column(Integer, ForeignKey('avatars.id'), nullable=True)
#     avatar = relationship("Avatar", foreign_keys=[avatar_id])
#     student_profile = relationship("Student", uselist=False, back_populates="user")
#     teacher_profile = relationship("Teacher", uselist=False, back_populates="user")
#     owned_avatars = relationship("Avatar", backref="owner", foreign_keys="Avatar.user_id")
    
#     achievements = relationship("StudentAchievement", back_populates="student")


# class Student(Base):
#     __tablename__ = "students"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
#     xp = Column(Integer, default=0, nullable=False)
#     level = Column(Integer, default=1, nullable=False)
#     district_id = Column(Integer, ForeignKey('districts.id'), nullable=True)
#     currency = Column(Integer, default=0, nullable=False)
    
#     user = relationship("User", back_populates="student_profile")
#     district = relationship("District")
#     courses = relationship("Course", secondary=student_course_association, back_populates="students")

#     # ДОБАВИТЬ это отношение
#     achievements = relationship("UserAchievement", back_populates="student")

# class Teacher(Base):
#     __tablename__ = "teachers"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
#     bio = Column(Text, nullable=True)
#     district_id = Column(Integer, ForeignKey('districts.id'), nullable=True)
    
#     # Отношения
#     user = relationship("User", back_populates="teacher_profile")
#     district = relationship("District")
#     courses = relationship("Course", back_populates="teacher")

# class District(Base):
#     __tablename__ = "districts"
    
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(Text, nullable=True)
    
#     students = relationship("Student", back_populates="district")
#     teachers = relationship("Teacher", back_populates="district")
#     courses = relationship("Course", back_populates="district")
    


# class Courses(Base):
#     __tablename__ = "courses"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     district_id = Column(Integer, ForeignKey('districts.id'), nullable=False)
#     teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
#     xp_reward = Column(Integer, default=0, nullable=False)
#     price = Column(Integer, default=0, nullable=False)
    
#     district = relationship("District", back_populates="courses")
#     teacher = relationship("Teacher", back_populates="courses")
#     students = relationship("Student", secondary=student_course_association, back_populates="courses")
#     topics = relationship("Topic", back_populates="course")

    




# class Topic(Base):
#     __tablename__ = "topics"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
#     xp_reward = Column(Integer, default=0, nullable=False)
#     order_index = Column(Integer, nullable=False)
    

#     course = relationship("Course", back_populates="topics")
#     completions = relationship("StudentTopicCompletion", back_populates="topic")


# class StudentTopicCompletion(Base):
#     __tablename__ = "student_topic_completions"
    
#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
#     topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
#     completion_date = Column(DateTime, default=datetime.utcnow, nullable=False)
#     xp_earned = Column(Integer, nullable=False)
    

#     student = relationship("Student")
#     topic = relationship("Topic", back_populates="completions")



# class UserAchievement(Base):
#     __tablename__ = "user_achievements"
    
#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
#     achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False)
#     unlock_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    

#     student = relationship("User", back_populates="achievements")
#     achievement = relationship("Achievement")

# class Achievement(Base):
#     __tablename__ = "achievements"
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     icon_url = Column(String, nullable=False)
    

    
    
# class Title(Base):
#     __tablename__ = "titles"
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     description = Column(Text, nullable=True)

# class LevelReward(Base):
#     __tablename__ = "level_rewards"
    
#     id = Column(Integer, primary_key=True)
#     level = Column(Integer, unique=True, nullable=False)
#     reward_description = Column(Text, nullable=False)
#     currency_reward = Column(Integer, default=0, nullable=False)
    


# class WeeklyLeaderboard(Base):
#     __tablename__ = "weekly_leaderboard"
    
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     week_start = Column(DateTime, nullable=False)
#     xp_earned = Column(Integer, default=0, nullable=False)
    
#     # Отношения
#     user = relationship("User")


# class Avatar(Base):
#     __tablename__ = "avatars"
    
#     id = Column(Integer, primary_key=True)
#     filename = Column(String, nullable=False)  # Имя файла на сервере
#     is_default = Column(Boolean, default=False, nullable=False)  # Стандартная аватарка
#     is_public = Column(Boolean, default=False, nullable=False)  # Доступна ли всем
#     price = Column(Integer, default=0, nullable=False)  # Цена во внутренней валюте
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    