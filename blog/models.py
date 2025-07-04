from sqlalchemy import Integer, Column, String, Boolean
from .database import Base

class Blog(Base):
    __tablename__="blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body=Column(String)
    published = Column(Boolean, default=True) 

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)