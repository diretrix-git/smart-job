from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.skill import user_skills

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("Skill", secondary=user_skills, backref="users")
