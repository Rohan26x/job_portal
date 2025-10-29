from pydantic import BaseModel, Field
from typing import Optional


class JobSeekerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None


class JobSeekerCreate(JobSeekerBase):
    pass


class JobSeekerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = None


class JobSeekerResponse(JobSeekerBase):
    seeker_id: int
    user_id: int
    resume_id: Optional[int] = None

    class Config:
        from_attributes = True
