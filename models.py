from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from static import Roles


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    login = Column(String,index=True)
    password = Column(String)
    last_activity_date = Column(DateTime)
    creation_date = Column(DateTime)
    role = Column(Enum(Roles))
    
    district = relationship("District")


class District(Base):
    __tablename__ = "districts"
    
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    
    
