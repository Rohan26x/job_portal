from fastapi import File, UploadFile
import os
from pathlib import Path

RESUME_UPLOAD_DIR = Path("backend/uploads/resumes")
RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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
