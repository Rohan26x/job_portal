from pydantic import BaseModel
from datetime import date
from typing import Optional

class ApplicationCreate(BaseModel):
    job_id: int

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

class ApplicationResponse(BaseModel):
    application_id: int
    job_id: int
    job_seeker_id: int  # Changed from seeker_id
    status: str
    application_date: Optional[date] = None

    class Config:
        from_attributes = True
