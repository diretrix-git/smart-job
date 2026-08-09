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
    skill_score: float
    semantic_score: float
    final_score: float
    match_score: float
    matched_required_skills: List[str]
    missing_required_skills: List[str]
    matched_preferred_skills: List[str]
    missing_preferred_skills: List[str]
    missing_skills: List[str]

class RecommendationOut(RecommendationBase):
    id: Optional[int] = None
    user_id: int
    job: JobOut
    created_at: Optional[datetime] = None
    recommended_courses: Optional[List[CourseRecommendation]] = []

    class Config:
        from_attributes = True
