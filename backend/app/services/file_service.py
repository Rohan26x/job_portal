import os
import shutil
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
from typing import Optional


class FileService:
    """Service for file upload operations"""

    UPLOAD_DIR = Path("app/uploads/resumes")
    ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file"""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in FileService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(FileService.ALLOWED_EXTENSIONS)}"
            )

    @staticmethod
    async def save_resume_file(file: UploadFile, seeker_id: int) -> str:
        """Save uploaded resume file"""
        FileService.validate_file(file)

        # Create upload directory if not exists
        FileService.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        file_ext = Path(file.filename).suffix
        filename = f"resume_{seeker_id}_{file.filename}"
        file_path = FileService.UPLOAD_DIR / filename

        # Save file
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )

        return str(file_path)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False
