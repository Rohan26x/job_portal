from pydantic import BaseModel, Field


class EducationBase(BaseModel):
    school_name: str = Field(..., min_length=1, max_length=200)
    degree: str = Field(..., min_length=1, max_length=200)


class EducationCreate(EducationBase):
    resume_id: int


class EducationUpdate(EducationBase):
    pass


class EducationResponse(EducationBase):
    education_id: int
    resume_id: int

    class Config:
        from_attributes = True
