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


@router.get("/me", response_model=ResumeResponse)
def get_my_resume(
    current_user=Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Get resume for the current authenticated job seeker"""
    resume = ResumeService.get_resume_by_job_seeker(db, current_user.user_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found for user")
    # Prepare skills and certifications for serialization if needed
    resume_data = ResumeResponse(
        resume_id=resume.resume_id,
        job_seeker_id=resume.job_seeker_id,
        about_me=resume.about_me,
        resume_skills=[{"skill_name": skill.skill_name} for skill in getattr(resume, 'skills', [])],
        certifications=[
            {
                "cert_name": cert.cert_name,
                "issuing_organization": cert.issuing_organization
            } for cert in getattr(resume, 'certifications', [])
        ]
    )
    return resume_data


@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    current_user=Depends(get_current_job_seeker),
    db: Session = Depends(get_db)
):
    """Update an existing resume by ID for the current user"""
    resume = ResumeService.update_resume(db, resume_id, current_user.user_id, resume_update)
    # Prepare skills and certifications for serialization if needed
    resume_data = ResumeResponse(
        resume_id=resume.resume_id,
        job_seeker_id=resume.job_seeker_id,
        about_me=resume.about_me,
        resume_skills=[{"skill_name": skill.skill_name} for skill in getattr(resume, 'skills', [])],
        certifications=[
            {
                "cert_name": cert.cert_name,
                "issuing_organization": cert.issuing_organization
            } for cert in getattr(resume, 'certifications', [])
        ]
    )
    return resume_data

# ... rest of your endpoints below
