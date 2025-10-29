from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, unique=True, nullable=False, index=True)
    skill_type = Column(String, nullable=True)

    # Relationships
    resume_skills = relationship("ResumeSkill", back_populates="skill", cascade="all, delete-orphan")
