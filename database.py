import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Students(Base):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), nullable = False)
    password = Column(String(100), nullable = False)

class staff(Base):
    __tablename__ = 'staff'
    id  = Column(Integer, primary_key = True)

class Water(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key = True)

class Mess(Base):
    __tablename__ = 'mess'
    id = Column(Integer, primary_key = True)

class Facilities(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key = True)

class Others(Base):
    __tablename__ = 'others'
    id = Column(Integer, primary_key = True)

engine = create_engine('sqlite:///feedback.db')
Base.metadata.create_all(engine)
