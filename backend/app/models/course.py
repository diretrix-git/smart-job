from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.skill import course_skills

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    url = Column(String, nullable=False)

    skills = relationship("Skill", secondary=course_skills, backref="courses")
