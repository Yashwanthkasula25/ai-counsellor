from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean # 👈 Added Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    current_stage = Column(String, default="ONBOARDING") 
    profile_summary = Column(Text, default="") 

    shortlist = relationship("UserShortlist", back_populates="user")

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    ranking = Column(Integer)

class UserShortlist(Base):
    __tablename__ = "user_shortlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    university_id = Column(Integer, ForeignKey("universities.id"))
    category = Column(String) 
    ai_reasoning = Column(Text)
    is_locked = Column(Boolean, default=False) # 👈 NEW FIELD

    user = relationship("User", back_populates="shortlist")
    university = relationship("University")