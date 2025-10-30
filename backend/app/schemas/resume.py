from pydantic import BaseModel
from typing import List, Optional

class CertificationCreate(BaseModel):
    cert_name: str
    issuing_organization: str

class ResumeCreate(BaseModel):
    about_me: Optional[str] = None
    skills: List[str] = []
    certifications: List[CertificationCreate] = []

class ResumeUpdate(BaseModel):
    about_me: Optional[str] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[CertificationCreate]] = None

class ResumeResponse(BaseModel):
    resume_id: int
    job_seeker_id: int
    about_me: Optional[str] = None
    resume_skills: Optional[List[dict]] = []
    certifications: Optional[List[CertificationCreate]] = []

    class Config:
        from_attributes = True
