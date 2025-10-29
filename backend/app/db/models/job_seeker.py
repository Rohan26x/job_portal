from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class JobSeeker(Base):
    __tablename__ = "job_seekers"

    seeker_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="job_seeker")
    resumes = relationship("Resume", back_populates="job_seeker", foreign_keys="Resume.seeker_id")
    applications = relationship("Application", back_populates="job_seeker", cascade="all, delete-orphan")
