from pydantic import BaseModel, Field
from typing import Optional


class RecruiterBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200)
    company_description: Optional[str] = None


class RecruiterCreate(RecruiterBase):
    pass


class RecruiterUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=200)
    company_description: Optional[str] = None


class RecruiterResponse(RecruiterBase):
    recruiter_id: int
    user_id: int

    class Config:
        from_attributes = True
