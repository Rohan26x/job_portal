from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.recruiter import Recruiter
from app.db.models.user import User
from app.schemas.recruiter import RecruiterUpdate


class RecruiterService:
    """Service for recruiter operations"""

    @staticmethod
    def get_recruiter_by_user_id(db: Session, user_id: int) -> Recruiter:
        """Get recruiter profile by user ID"""
        recruiter = db.query(Recruiter).filter(Recruiter.user_id == user_id).first()
        if not recruiter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recruiter profile not found"
            )
        return recruiter

    @staticmethod
    def get_recruiter_by_id(db: Session, recruiter_id: int) -> Recruiter:
        """Get recruiter by recruiter ID"""
        recruiter = db.query(Recruiter).filter(Recruiter.recruiter_id == recruiter_id).first()
        if not recruiter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recruiter not found"
            )
        return recruiter

    @staticmethod
    def update_recruiter(db: Session, user_id: int, update_data: RecruiterUpdate) -> Recruiter:
        """Update recruiter profile"""
        recruiter = RecruiterService.get_recruiter_by_user_id(db, user_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(recruiter, key, value)

        db.commit()
        db.refresh(recruiter)
        return recruiter
