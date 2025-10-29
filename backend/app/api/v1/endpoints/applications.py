from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from app.services.application_service import ApplicationService
from app.services.job_seeker_service import JobSeekerService
from app.services.job_service import JobService
from app.core.dependencies import get_current_job_seeker, get_current_recruiter, get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(
    app_data: ApplicationCreate,
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Apply for a job (job seeker only)"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    return ApplicationService.create_application(db, app_data, job_seeker.seeker_id)

@router.get("/my-applications", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Get all applications by current job seeker"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    return ApplicationService.get_applications_by_seeker(db, job_seeker.seeker_id)

@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def get_applications_for_job(
    job_id: int,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get all applications for a job (recruiter only)"""
    # Verify job belongs to recruiter
    job = JobService.get_job_by_id(db, job_id)
    return ApplicationService.get_applications_by_job(db, job_id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    update_data: ApplicationUpdate,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update application status (recruiter only)"""
    return ApplicationService.update_application_status(db, application_id, update_data)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(
    application_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application details by ID"""
    return ApplicationService.get_application_by_id(db, application_id)
