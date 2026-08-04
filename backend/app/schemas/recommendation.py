from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.job import JobOut

class CourseRecommendation(BaseModel):
    title: str
    provider: str
    url: str

class RecommendationBase(BaseModel):
    job_id: int
    match_score: float
    missing_skills: List[str]

class RecommendationOut(RecommendationBase):
    id: Optional[int] = None
    user_id: int
    job: JobOut
    created_at: Optional[datetime] = None
    recommended_courses: Optional[List[CourseRecommendation]] = []

    class Config:
        from_attributes = True
