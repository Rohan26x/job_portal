from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.db.models.skill import resume_skills_association


class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    job_seeker_id = Column(Integer, ForeignKey("job_seekers.job_seeker_id"), unique=True, nullable=False)
    about_me = Column(Text)

    # Relationships
    job_seeker = relationship("JobSeeker", back_populates="resume")
    resume_skills = relationship("Skill", secondary=resume_skills_association)
    certifications = relationship("Certification", back_populates="resume", cascade="all, delete-orphan")


class Certification(Base):
    __tablename__ = "certifications"

    cert_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    cert_name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=False)

    resume = relationship("Resume", back_populates="certifications")
