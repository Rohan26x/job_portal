from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import date
from app.db.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate


class ApplicationService:
    """Service for application operations"""

    @staticmethod
    def create_application(db: Session, app_data: ApplicationCreate, seeker_id: int) -> Application:
        """Create a new job application"""
        # Check if already applied
        existing = db.query(Application).filter(
            Application.job_id == app_data.job_id,
            Application.seeker_id == seeker_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already applied to this job"
            )

        db_application = Application(
            job_id=app_data.job_id,
            seeker_id=seeker_id,
            application_date=date.today(),
            status=ApplicationStatus.pending
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def get_application_by_id(db: Session, application_id: int) -> Application:
        """Get application by ID"""
        application = db.query(Application).filter(
            Application.application_id == application_id
        ).first()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        return application

    @staticmethod
    def get_applications_by_job(db: Session, job_id: int) -> List[Application]:
        """Get all applications for a job"""
        return db.query(Application).filter(Application.job_id == job_id).all()

    @staticmethod
    def get_applications_by_seeker(db: Session, seeker_id: int) -> List[Application]:
        """Get all applications by a job seeker"""
        return db.query(Application).filter(Application.seeker_id == seeker_id).all()

    @staticmethod
    def update_application_status(
            db: Session,
            application_id: int,
            update_data: ApplicationUpdate
    ) -> Application:
        """Update application status (recruiter only)"""
        application = ApplicationService.get_application_by_id(db, application_id)

        application.status = update_data.status
        db.commit()
        db.refresh(application)
        return application
