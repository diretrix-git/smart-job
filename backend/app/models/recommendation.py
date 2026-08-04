from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    missing_skills = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    job = relationship("Job", back_populates="recommendations")
