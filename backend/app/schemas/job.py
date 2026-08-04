from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.skill import SkillOut

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    company_url: Optional[str] = None

class JobCreate(JobBase):
    skill_names: List[str]

class JobOut(JobBase):
    id: int
    created_at: datetime
    skills: List[SkillOut] = []

    class Config:
        from_attributes = True
