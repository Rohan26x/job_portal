from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db.database import get_db
from app.services.ai_service import AIService
from app.services.job_seeker_service import JobSeekerService
from app.services.file_service import FileService
from app.core.dependencies import get_current_job_seeker
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Features"])


class JobSearchRequest(BaseModel):
    search_description: str


@router.post("/parse-resume")
async def parse_resume(
        file: UploadFile = File(...),
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Parse resume using AI and extract structured information"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)

    # Save file temporarily
    file_path = await FileService.save_resume_file(file, job_seeker.seeker_id)

    # Parse with AI
    parsed_data = AIService.parse_uploaded_resume(file_path)

    return {
        "message": "Resume parsed successfully",
        "data": parsed_data
    }


@router.get("/job-recommendations")
def get_job_recommendations(
        limit: int = 10,
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Get AI-powered job recommendations based on resume"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    recommendations = AIService.get_job_recommendations(db, job_seeker.seeker_id, limit)

    return {
        "recommendations": recommendations,
        "count": len(recommendations)
    }


@router.post("/intelligent-search")
def intelligent_job_search(
        search_request: JobSearchRequest,
        db: Session = Depends(get_db)
):
    """AI-powered job search using natural language description"""
    results = AIService.intelligent_job_search(db, search_request.search_description)

    return {
        "results": results,
        "count": len(results),
        "query": search_request.search_description
    }
