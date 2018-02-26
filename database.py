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
    Caretaker = Column(String(20), nullable = False)
    Wardens = Column(String(20), nullable = False)
    Principal= Column(String(20), nullable = False)
    Behaviour = Column(String(20), nullable = False)
    Problems = Column(String(20), nullable = False)
    Rating = Column(String(20), nullable = False)

class Water(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key = True)
    Water = Column(String(20), nullable = False)
    Quality= Column(String(20), nullable = False)
    Quantity = Column(String(20), nullable = False)
    Variety = Column(String(20), nullable = False)
    Cost = Column(String(20), nullable = False)

class Mess(Base):
    __tablename__ = 'mess'
    id = Column(Integer, primary_key = True)
    Morning = Column(String(20), nullable = False)
    Afternoon = Column(String(20), nullable = False)
    Evening = Column(String(20), nullable = False)
    Dinner = Column(String(20), nullable = False)
    Availablity = Column(String(20), nullable = False)
    Quality = Column(String(20), nullable = False)
    Behaviour = Column(String(20), nullable = False)

class FacilitiesFeedback(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key = True)
    Room = Column(String(20), nullable = False)
    Corridors = Column(String(20), nullable = False)
    Toilets = Column(String(20), nullable = False)
    Croom = Column(String(20), nullable = False)
    Lawns = Column(String(20), nullable = False)

class OtherFeedback(Base):
    __tablename__ = 'others'
    id = Column(Integer, primary_key = True)
    Availability = Column(String(20), nullable = False)
    Services = Column(String(20), nullable = False)

engine = create_engine('sqlite:///feedback.db')
Base.metadata.create_all(engine)
