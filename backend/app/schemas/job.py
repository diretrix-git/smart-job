from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.skill import SkillOut



class JobBase(BaseModel):
    title: str
    description: str
    company: str
    company_url: Optional[str] = None

class JobSkillOut(BaseModel):
    skill: SkillOut
    importance: str

    class Config:
        from_attributes = True

class JobOut(JobBase):
    id: int
    created_at: datetime
    job_skills: List[JobSkillOut] = []

    class Config:
        from_attributes = True
