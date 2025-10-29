from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum
from datetime import date


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    accepted = "accepted"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    seeker_id = Column(Integer, ForeignKey("job_seekers.seeker_id", ondelete="CASCADE"), nullable=False)
    application_date = Column(Date, default=date.today, nullable=False)
    status = Column(ENUM(ApplicationStatus, name='applicationstatus', create_type=False),
                    default=ApplicationStatus.pending, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="applications")
    job_seeker = relationship("JobSeeker", back_populates="applications")
