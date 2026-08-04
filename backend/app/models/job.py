from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.skill import job_skills

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    company_url = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship("Skill", secondary=job_skills, backref="jobs")
    recommendations = relationship("Recommendation", back_populates="job", cascade="all, delete-orphan")
