from pydantic import BaseModel
from typing import List
from app.schemas.skill import SkillOut

class CourseBase(BaseModel):
    title: str
    provider: str
    url: str

class CourseOut(CourseBase):
    id: int
    skills: List[SkillOut] = []

    class Config:
        from_attributes = True
