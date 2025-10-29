from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Recruiter(Base):
    __tablename__ = "recruiters"

    recruiter_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    company_description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="recruiter")
    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")
