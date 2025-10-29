from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.resume import ResumeResponse, ResumeCreate, ResumeUpdate
from app.services.resume_service import ResumeService
from app.services.job_seeker_service import JobSeekerService
from app.services.file_service import FileService
from app.core.dependencies import get_current_job_seeker

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/", response_model=ResumeResponse, status_code=201)
def create_resume(
        resume_data: ResumeCreate,
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Create a new resume (job seeker only)"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    return ResumeService.create_resume(db, resume_data, job_seeker.seeker_id)


@router.post("/upload", response_model=dict)
async def upload_resume_file(
        file: UploadFile = File(...),
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Upload resume file (PDF, DOC, DOCX)"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    file_path = await FileService.save_resume_file(file, job_seeker.seeker_id)

    # Update or create resume with file path
    try:
        resume = ResumeService.get_resume_by_seeker(db, job_seeker.seeker_id)
        resume.file_path = file_path
        db.commit()
    except:
        resume = ResumeService.create_resume(
            db,
            ResumeCreate(about_me=None),
            job_seeker.seeker_id
        )
        resume.file_path = file_path
        db.commit()

    return {"message": "Resume uploaded successfully", "file_path": file_path}


@router.get("/me", response_model=ResumeResponse)
def get_my_resume(
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Get current job seeker's resume"""
    job_seeker = JobSeekerService.get_job_seeker_by_user_id(db, current_user.user_id)
    return ResumeService.get_resume_by_seeker(db, job_seeker.seeker_id)


@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
        resume_id: int,
        update_data: ResumeUpdate,
        current_user=Depends(get_current_job_seeker),
        db: Session = Depends(get_db)
):
    """Update resume"""
    return ResumeService.update_resume(db, resume_id, update_data)


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume_by_id(
        resume_id: int,
        db: Session = Depends(get_db)
):
    """Get resume by ID"""
    return ResumeService.get_resume_by_id(db, resume_id)
