from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.database import get_db
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse
from app.services.resume_service import ResumeService
from app.core.dependencies import get_current_job_seeker

# Define router FIRST (this was missing)
router = APIRouter(prefix="/resumes", tags=["Resumes"])

# Create uploads directory
RESUME_UPLOAD_DIR = Path("backend/uploads/resumes")
RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# NOW define all your endpoints below
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
        file: UploadFile = File(...),
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Upload a resume file"""
    if not file.filename.endswith(('.pdf', '.doc', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC, and DOCX files are allowed"
        )

    file_path = RESUME_UPLOAD_DIR / f"{current_user.user_id}_{file.filename}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": "Resume uploaded successfully", "filename": file.filename}


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
def create_resume(
        resume_data: ResumeCreate,
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Create a new resume"""
    return ResumeService.create_resume(db, current_user.user_id, resume_data)

# ... rest of your endpoints below
