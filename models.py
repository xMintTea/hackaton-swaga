from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # author = relationship("User") <- поместить экзепляор класса пользователя. В схемах тоже должно быть такое же
    
    
