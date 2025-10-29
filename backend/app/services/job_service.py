from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.db.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class JobService:
    """Service for job operations"""

    @staticmethod
    def create_job(db: Session, job_data: JobCreate, recruiter_id: int) -> Job:
        """Create a new job posting"""
        db_job = Job(
            job_title=job_data.job_title,
            description=job_data.description,
            location=job_data.location,
            recruiter_id=recruiter_id
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def get_job_by_id(db: Session, job_id: int) -> Job:
        """Get job by ID"""
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        return job

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get all jobs with pagination"""
        return db.query(Job).offset(skip).limit(limit).all()

    @staticmethod
    def get_jobs_by_recruiter(db: Session, recruiter_id: int) -> List[Job]:
        """Get all jobs posted by a recruiter"""
        return db.query(Job).filter(Job.recruiter_id == recruiter_id).all()

    @staticmethod
    def update_job(db: Session, job_id: int, recruiter_id: int, update_data: JobUpdate) -> Job:
        """Update a job posting"""
        job = JobService.get_job_by_id(db, job_id)

        # Verify job belongs to recruiter
        if job.recruiter_id != recruiter_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this job"
            )

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(job, key, value)

        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def delete_job(db: Session, job_id: int, recruiter_id: int) -> bool:
        """Delete a job posting"""
        job = JobService.get_job_by_id(db, job_id)

        # Verify job belongs to recruiter
        if job.recruiter_id != recruiter_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this job"
            )

        db.delete(job)
        db.commit()
        return True

    @staticmethod
    def search_jobs(db: Session, query: str, location: Optional[str] = None) -> List[Job]:
        """Search jobs by title and location"""
        jobs_query = db.query(Job)

        if query:
            jobs_query = jobs_query.filter(Job.job_title.ilike(f"%{query}%"))

        if location:
            jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))

        return jobs_query.all()
