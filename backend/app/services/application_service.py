from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.application import Application, ApplicationStatus
from app.db.models.job import Job
from app.db.models.job_seeker import JobSeeker


class ApplicationService:
    """Service for managing job applications"""

    @staticmethod
    def create_application(db: Session, job_id: int, job_seeker_id: int):
        """Create a new job application"""
        # Check if job exists
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )

        # Check if application already exists
        existing_application = db.query(Application).filter(
            Application.job_id == job_id,
            Application.job_seeker_id == job_seeker_id
        ).first()

        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this job"
            )

        # Create new application
        application = Application(
            job_id=job_id,
            job_seeker_id=job_seeker_id,
            status=ApplicationStatus.pending
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return application

    @staticmethod
    def get_applications_by_job(db: Session, job_id: int):
        """Get all applications for a specific job"""
        return db.query(Application).filter(Application.job_id == job_id).all()

    @staticmethod
    def get_applications_by_seeker(db: Session, job_seeker_id: int):
        """Get all applications by a job seeker"""
        return db.query(Application).filter(Application.job_seeker_id == job_seeker_id).all()  # CHANGED HERE

    @staticmethod
    def update_application_status(db: Session, application_id: int, new_status: str):
        """Update application status"""
        application = db.query(Application).filter(
            Application.application_id == application_id
        ).first()

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )

        # Validate status
        try:
            status_enum = ApplicationStatus(new_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {[s.value for s in ApplicationStatus]}"
            )

        application.status = status_enum
        db.commit()
        db.refresh(application)

        return application

    @staticmethod
    def get_application_by_id(db: Session, application_id: int):
        """Get application by ID"""
        return db.query(Application).filter(
            Application.application_id == application_id
        ).first()
