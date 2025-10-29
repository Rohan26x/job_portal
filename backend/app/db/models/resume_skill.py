from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    resume_skill_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="resume_skills")
    skill = relationship("Skill", back_populates="resume_skills")
