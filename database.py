import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as phash

Base = declarative_base()

class Admins(Base):
    __tablename__ = 'Admin'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), nullable = False, index=True)
    password_hash = Column(String(100))

    def hash_password(self, password):
        self.password_hash = phash.encrypt(password)

    def verify_password(self, password):
        return phash.verify(password, self.password_hash)

class Students(Base):
    __tablename__ = 'Student'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(50), nullable = False, index=True)
    password_hash = Column(String(100))

    def hash_password(self, password):
        self.password_hash = phash.encrypt(password)

    def verify_password(self, password):
        return phash.verify(password, self.password_hash)

class staff(Base):
    __tablename__ = 'staff'
    id  = Column(Integer, primary_key = True)
    Caretaker = Column(Integer, nullable = False)
    Wardens = Column(Integer, nullable = False)
    Principal= Column(Integer, nullable = False)
    Behaviour = Column(Integer, nullable = False)
    Problems = Column(Integer, nullable = False)
    Rating = Column(Integer, nullable = False)

class Water(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key = True)
    Water = Column(Integer, nullable = False)
    Quality= Column(Integer, nullable = False)
    Quantity = Column(Integer, nullable = False)
    Variety = Column(Integer, nullable = False)
    Cost = Column(Integer, nullable = False)

class Mess(Base):
    __tablename__ = 'mess'
    id = Column(Integer, primary_key = True)
    Morning = Column(Integer, nullable = False)
    Afternoon = Column(Integer, nullable = False)
    Evening = Column(Integer, nullable = False)
    Dinner = Column(Integer, nullable = False)
    Availability = Column(Integer, nullable = False)
    Quality = Column(Integer, nullable = False)
    Behaviour = Column(Integer, nullable = False)

class FacilitiesFeedback(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key = True)
    Room = Column(Integer, nullable = False)
    Corridors = Column(Integer, nullable = False)
    Toilets = Column(Integer, nullable = False)
    Croom = Column(Integer, nullable = False)
    Lawns = Column(Integer, nullable = False)

class OtherFeedback(Base):
    __tablename__ = 'others'
    id = Column(Integer, primary_key = True)
    Availability = Column(Integer, nullable = False)
    Services = Column(Integer, nullable = False)

engine = create_engine('sqlite:///feedback.db')
Base.metadata.create_all(engine)
