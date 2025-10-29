from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.recruiter_id", ondelete="CASCADE"), nullable=False)

    # Relationships
    recruiter = relationship("Recruiter", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
