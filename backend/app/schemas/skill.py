from pydantic import BaseModel, Field
from typing import Optional


class SkillBase(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=100)
    skill_type: Optional[str] = Field(None, max_length=50)


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    skill_id: int

    class Config:
        from_attributes = True
