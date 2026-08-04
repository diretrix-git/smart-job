from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    raw_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
