from pydantic import BaseModel, Field
from typing import Optional


class JobBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    location: str = Field(..., min_length=1, max_length=200)


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    job_title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = Field(None, min_length=1, max_length=200)


class JobResponse(JobBase):
    job_id: int
    recruiter_id: int

    class Config:
        from_attributes = True
