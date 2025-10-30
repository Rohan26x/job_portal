from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class JobSeeker(Base):
    __tablename__ = "job_seekers"

    job_seeker_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    bio = Column(Text)
    # Removed created_at and updated_at since they don't exist in database

    # Relationships
    user = relationship("User", back_populates="job_seeker")
    resume = relationship("Resume", back_populates="job_seeker", uselist=False)
    applications = relationship("Application", back_populates="job_seeker")
