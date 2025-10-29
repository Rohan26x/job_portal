from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    seeker_id = Column(Integer, ForeignKey("job_seekers.seeker_id", ondelete="CASCADE"), nullable=False)
    about_me = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)

    # Relationships
    job_seeker = relationship("JobSeeker", back_populates="resumes", foreign_keys=[seeker_id])
    educations = relationship("Education", back_populates="resume", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="resume", cascade="all, delete-orphan")
    resume_skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
