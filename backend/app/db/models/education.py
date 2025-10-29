from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Education(Base):
    __tablename__ = "educations"

    education_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False)
    school_name = Column(String, nullable=False)
    degree = Column(String, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="educations")
