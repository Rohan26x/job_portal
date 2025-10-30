from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("recruiters.recruiter_id"), nullable=False)
    job_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    # REMOVED: posted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recruiter = relationship("Recruiter", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    job_skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
