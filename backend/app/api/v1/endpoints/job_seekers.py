from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.job_seeker import JobSeekerResponse, JobSeekerUpdate
from app.services.job_seeker_service import JobSeekerService
from app.core.dependencies import get_current_job_seeker

router = APIRouter(prefix="/job-seekers", tags=["Job Seekers"])

@router.get("/me", response_model=JobSeekerResponse)
def get_my_job_seeker_profile(
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Get current job seeker's profile"""
    return JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)

@router.put("/me", response_model=JobSeekerResponse)
def update_my_job_seeker_profile(
    update_data: JobSeekerUpdate,
    current_user = Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Update current job seeker's profile"""
    return JobSeekerService.update_job_seeker(db, current_user.user_id, update_data)

@router.get("/{seeker_id}", response_model=JobSeekerResponse)
def get_job_seeker_by_id(
    seeker_id: int,
    db: Session = Depends(get_db)
):
    """Get job seeker profile by ID"""
    return JobSeekerService.get_job_seeker_by_id(db, seeker_id)
