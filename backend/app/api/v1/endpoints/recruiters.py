from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.recruiter import RecruiterResponse, RecruiterUpdate
from app.services.recruiter_service import RecruiterService
from app.core.dependencies import get_current_recruiter

router = APIRouter(prefix="/recruiters", tags=["Recruiters"])

@router.get("/me", response_model=RecruiterResponse)
def get_my_recruiter_profile(
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get current recruiter's profile"""
    return RecruiterService.get_recruiter_by_user_id(db, current_user.user_id)

@router.put("/me", response_model=RecruiterResponse)
def update_my_recruiter_profile(
    update_data: RecruiterUpdate,
    current_user = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update current recruiter's profile"""
    return RecruiterService.update_recruiter(db, current_user.user_id, update_data)

@router.get("/{recruiter_id}", response_model=RecruiterResponse)
def get_recruiter_by_id(
    recruiter_id: int,
    db: Session = Depends(get_db)
):
    """Get recruiter profile by ID (public)"""
    return RecruiterService.get_recruiter_by_id(db, recruiter_id)
