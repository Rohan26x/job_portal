from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class UserType(str, enum.Enum):
    recruiter = "recruiter"
    job_seeker = "job_seeker"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_type = Column(ENUM(UserType, name='usertype', create_type=False), nullable=False)

    # Relationships
    recruiter = relationship("Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan")
    job_seeker = relationship("JobSeeker", back_populates="user", uselist=False, cascade="all, delete-orphan")
