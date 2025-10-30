from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), unique=True, nullable=False)

    # Relationships
    resume_skills = relationship("ResumeSkill", back_populates="skill", cascade="all, delete-orphan")
    job_skills = relationship("JobSkill", back_populates="skill", cascade="all, delete-orphan")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    resume_skill_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="resume_skills")
    skill = relationship("Skill", back_populates="resume_skills")


class JobSkill(Base):
    __tablename__ = "job_skills"

    job_skill_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)

    # Relationships
    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")
