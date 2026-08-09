import json
import os
import sys
import math
import os
import sys

# Add parent directory to path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import engine, Base, SessionLocal
from app.models.skill import Skill, JobSkill
from app.models.job import Job
from app.models.course import Course

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def load_json(filename: str):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as f:
        return json.load(f)

def seed_db():
    print("Dropping and recreating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = get_db()

    print("Seeding skills...")
    skills_data = load_json('skills.json')
    skill_objects = {}
    for item in skills_data:
        skill = db.query(Skill).filter(Skill.name == item['name']).first()
        if not skill:
            skill = Skill(name=item['name'], category=item['category'])
            db.add(skill)
            db.commit()
            db.refresh(skill)
        skill_objects[skill.name] = skill

    print("Seeding jobs...")
    jobs_data = load_json('jobs.json')
    for item in jobs_data:
        job = db.query(Job).filter(Job.title == item['title'], Job.company == item['company']).first()
        if not job:
            job = Job(
                title=item['title'], 
                description=item['description'], 
                company=item['company'],
                company_url=item.get('company_url')
            )
            skills_list = item['skills']
            req_count = math.ceil(len(skills_list) / 2)
            for idx, skill_name in enumerate(skills_list):
                if skill_name in skill_objects:
                    # Note: This required/preferred split is auto-generated as a placeholder,
                    # not curated by domain knowledge. This is a documented limitation of the current dataset.
                    importance = "required" if idx < req_count else "preferred"
                    js = JobSkill(skill=skill_objects[skill_name], importance=importance)
                    job.job_skills.append(js)
            db.add(job)

    print("Seeding courses...")
    courses_data = load_json('courses.json')
    for item in courses_data:
        course = db.query(Course).filter(Course.title == item['title']).first()
        if not course:
            course = Course(title=item['title'], provider=item['provider'], url=item['url'])
            for skill_name in item['skills']:
                if skill_name in skill_objects:
                    course.skills.append(skill_objects[skill_name])
            db.add(course)

    db.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_db()
