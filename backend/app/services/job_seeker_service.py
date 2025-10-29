from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.job_seeker import JobSeeker
from app.schemas.job_seeker import JobSeekerUpdate


class JobSeekerService:
    """Service for job seeker operations"""

    @staticmethod
    def get_job_seeker_by_user_id(db: Session, user_id: int) -> JobSeeker:
        """Get job seeker profile by user ID"""
        job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == user_id).first()
        if not job_seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job seeker profile not found"
            )
        return job_seeker

    @staticmethod
    def get_job_seeker_by_id(db: Session, seeker_id: int) -> JobSeeker:
        """Get job seeker by seeker ID"""
        job_seeker = db.query(JobSeeker).filter(JobSeeker.seeker_id == seeker_id).first()
        if not job_seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job seeker not found"
            )
        return job_seeker

    @staticmethod
    def update_job_seeker(db: Session, user_id: int, update_data: JobSeekerUpdate) -> JobSeeker:
        """Update job seeker profile"""
        job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, user_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(job_seeker, key, value)

        db.commit()
        db.refresh(job_seeker)
        return job_seeker
