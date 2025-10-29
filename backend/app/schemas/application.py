from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ApplicationBase(BaseModel):
    job_id: int


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|reviewed|accepted|rejected)$")


class ApplicationResponse(BaseModel):
    application_id: int
    job_id: int
    seeker_id: int
    application_date: date
    status: str

    class Config:
        from_attributes = True
