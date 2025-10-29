from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.services.job_service import JobService
from app.services.recruiter_service import RecruiterService
from app.core.dependencies import get_current_recruiter, get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    job_data: JobCreate,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Create a new job posting (recruiter only)"""
    recruiter = RecruiterService.get_recruiter_by_user_id(db, current_user.user_id)
    return JobService.create_job(db, job_data, recruiter.recruiter_id)

@router.get("/", response_model=List[JobResponse])
def get_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all job postings with pagination"""
    return JobService.get_all_jobs(db, skip, limit)

@router.get("/search", response_model=List[JobResponse])
def search_jobs(
    query: str = Query(None, min_length=1),
    location: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Search jobs by title and location"""
    return JobService.search_jobs(db, query, location)

@router.get("/my-jobs", response_model=List[JobResponse])
def get_my_jobs(
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get all jobs posted by current recruiter"""
    recruiter = RecruiterService.get_recruiter_by_user_id(db, current_user.user_id)
    return JobService.get_jobs_by_recruiter(db, recruiter.recruiter_id)

@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get job details by ID"""
    return JobService.get_job_by_id(db, job_id)

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update a job posting (recruiter only)"""
    recruiter = RecruiterService.get_recruiter_by_user_id(db, current_user.user_id)
    return JobService.update_job(db, job_id, recruiter.recruiter_id, job_data)

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Delete a job posting (recruiter only)"""
    recruiter = RecruiterService.get_recruiter_by_user_id(db, current_user.user_id)
    JobService.delete_job(db, job_id, recruiter.recruiter_id)
    return {"message": "Job deleted successfully"}
