from pydantic import BaseModel, Field


class CertificationBase(BaseModel):
    cert_name: str = Field(..., min_length=1, max_length=200)
    issuing_organization: str = Field(..., min_length=1, max_length=200)


class CertificationCreate(CertificationBase):
    resume_id: int


class CertificationUpdate(CertificationBase):
    pass


class CertificationResponse(CertificationBase):
    cert_id: int
    resume_id: int

    class Config:
        from_attributes = True
