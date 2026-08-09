"""
Recommendation engine: computes job match scores using a hybrid approach.
The final score is a weighted sum of:
  1. Skill Vector Similarity (Weight: 0.6) - Uses cosine similarity over 
     skill vectors where job skills are weighted (required = 1.0, preferred = 0.5)
     and user skills are binary (presence).
  2. Semantic Similarity (Weight: 0.4) - Uses sentence-transformers (all-MiniLM-L6-v2)
     to compute cosine similarity between the user's resume and the job description.

Limitations:
- Assumes skill independence (does not model substitutability).
- Does not explicitly model seniority level.
- The 0.6 / 0.4 weights are tunable placeholders and can be optimized.
"""
from typing import List, Set, Tuple, Dict
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
import numpy as np

from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User
from app.models.course import Course
from app.services.nlp_extractor import compute_semantic_score
from app.core.config import settings


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Uses sklearn's cosine_similarity to compute similarity between two vectors."""
    if not vec_a or not vec_b:
        return 0.0
    # sklearn expects 2D arrays
    arr_a = np.array(vec_a).reshape(1, -1)
    arr_b = np.array(vec_b).reshape(1, -1)
    
    norm_a = np.linalg.norm(arr_a)
    norm_b = np.linalg.norm(arr_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(sklearn_cosine_similarity(arr_a, arr_b)[0][0])


def build_skill_vectors(
    user_skill_ids: Set[int], job_skills: Dict[int, str]
) -> Tuple[List[float], List[float]]:
    """Builds weighted presence vectors over the union of both skill ID sets."""
    all_skill_ids = sorted(user_skill_ids | set(job_skills.keys()))
    user_vec = [1.0 if sid in user_skill_ids else 0.0 for sid in all_skill_ids]
    job_vec = []
    for sid in all_skill_ids:
        if sid in job_skills:
            job_vec.append(1.0 if job_skills[sid] == "required" else 0.5)
        else:
            job_vec.append(0.0)
    return user_vec, job_vec


def recommend_courses_for_skills(
    missing_skill_ids: Set[int], db: Session
) -> List[Course]:
    """Returns distinct courses that teach at least one of the missing skills."""
    if not missing_skill_ids:
        return []
    return (
        db.query(Course)
        .join(Course.skills)
        .filter(Skill.id.in_(missing_skill_ids))
        .distinct()
        .all()
    )


def calculate_job_matches(db: Session, current_user: User) -> List[dict]:
    """
    For the current user, scores every job by hybrid similarity (skills + semantic),
    finds missing skills, and attaches course recommendations.
    Returns results sorted by final_score descending.
    """
    user_skill_ids = {s.id for s in current_user.skills}
    jobs = db.query(Job).all()
    results = []

    # Get user's latest resume text for semantic scoring
    resume_text = ""
    if current_user.resumes:
        latest_resume = sorted(current_user.resumes, key=lambda r: r.uploaded_at, reverse=True)[0]
        resume_text = latest_resume.raw_text

    for job in jobs:
        # job.job_skills is a list of JobSkill associations
        job_skills_dict = {js.skill_id: js.importance for js in job.job_skills}
        if not job_skills_dict:
            continue

        user_vec, job_vec = build_skill_vectors(user_skill_ids, job_skills_dict)
        skill_score = cosine_similarity(user_vec, job_vec)
        
        semantic_score = compute_semantic_score(resume_text, job.description)
        final_score = (settings.SKILL_WEIGHT * skill_score) + (settings.SEMANTIC_WEIGHT * semantic_score)

        # Categorize skills
        matched_required = []
        missing_required = []
        matched_preferred = []
        missing_preferred = []
        missing_required_ids = set()
        
        for js in job.job_skills:
            if js.skill_id in user_skill_ids:
                if js.importance == "required":
                    matched_required.append(js.skill.name)
                else:
                    matched_preferred.append(js.skill.name)
            else:
                if js.importance == "required":
                    missing_required.append(js.skill.name)
                    missing_required_ids.add(js.skill_id)
                else:
                    missing_preferred.append(js.skill.name)

        courses = recommend_courses_for_skills(missing_required_ids, db)

        results.append({
            "job_id": job.id,
            "job": job,
            "user_id": current_user.id,
            "skill_score": round(skill_score, 4),
            "semantic_score": round(semantic_score, 4),
            "final_score": round(final_score, 4),
            "match_score": round(final_score, 4), # for backwards compatibility with the schema base
            "matched_required_skills": matched_required,
            "missing_required_skills": missing_required,
            "matched_preferred_skills": matched_preferred,
            "missing_preferred_skills": missing_preferred,
            "missing_skills": missing_required,
            "recommended_courses": [
                {"title": c.title, "provider": c.provider, "url": c.url}
                for c in courses
            ],
        })

    results.sort(key=lambda r: r["final_score"], reverse=True)
    return results