from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.services.application_service import ApplicationService
from app.core.dependencies import get_current_user, get_current_job_seeker, get_current_recruiter

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    from app.db.models.job_seeker import JobSeeker
    job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == current_user.user_id).first()
    return ApplicationService.create_application(db, application.job_id, job_seeker.job_seeker_id)

@router.get("/my-applications", response_model=list[ApplicationResponse])
def get_my_applications(
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Get all applications for the current job seeker"""
    from app.db.models.job_seeker import JobSeeker
    job_seeker = db.query(JobSeeker).filter(JobSeeker.user_id == current_user.user_id).first()
    return ApplicationService.get_applications_by_seeker(db, job_seeker.job_seeker_id)  # CHANGED HERE

@router.get("/job/{job_id}", response_model=list[ApplicationResponse])
def get_applications_for_job(
    job_id: int,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get all applications for a specific job (recruiter only)"""
    return ApplicationService.get_applications_by_job(db, job_id)

@router.put("/{application_id}/status")
def update_application_status(
    application_id: int,
    status: str,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update application status (recruiter only)"""
    return ApplicationService.update_application_status(db, application_id, status)
