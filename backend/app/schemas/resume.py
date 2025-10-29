from pydantic import BaseModel, Field
from typing import Optional, List


class EducationBase(BaseModel):
    school_name: str = Field(..., min_length=1, max_length=200)
    degree: str = Field(..., min_length=1, max_length=200)


class EducationCreate(EducationBase):
    pass


class EducationResponse(EducationBase):
    education_id: int
    resume_id: int

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    cert_name: str = Field(..., min_length=1, max_length=200)
    issuing_organization: str = Field(..., min_length=1, max_length=200)


class CertificationCreate(CertificationBase):
    pass


class CertificationResponse(CertificationBase):
    cert_id: int
    resume_id: int

    class Config:
        from_attributes = True


class ResumeBase(BaseModel):
    about_me: Optional[str] = None


class ResumeCreate(ResumeBase):
    educations: Optional[List[EducationCreate]] = []
    certifications: Optional[List[CertificationCreate]] = []
    skills: Optional[List[int]] = []  # List of skill IDs


class ResumeUpdate(BaseModel):
    about_me: Optional[str] = None


class ResumeResponse(ResumeBase):
    resume_id: int
    seeker_id: int
    file_path: Optional[str] = None
    educations: Optional[List[EducationResponse]] = []
    certifications: Optional[List[CertificationResponse]] = []

    class Config:
        from_attributes = True
