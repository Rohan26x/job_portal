from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Certification(Base):
    __tablename__ = "certifications"

    cert_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False)
    cert_name = Column(String, nullable=False)
    issuing_organization = Column(String, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="certifications")
