from pydantic import BaseModel
from datetime import datetime
from typing import List

class ResumeOut(BaseModel):
    id: int
    user_id: int
    raw_text: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ExtractedSkills(BaseModel):
    skills: List[str]
