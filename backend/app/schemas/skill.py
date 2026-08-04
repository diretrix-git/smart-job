from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True
