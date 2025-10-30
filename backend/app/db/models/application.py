from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=False)
    job_seeker_id = Column(Integer, ForeignKey("job_seekers.job_seeker_id"), nullable=False)
    application_date = Column(Date)
    status = Column(String)

    # Relationships
    job = relationship("Job", back_populates="applications")
    job_seeker = relationship("JobSeeker", back_populates="applications")
