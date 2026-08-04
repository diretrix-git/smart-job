"""
Recommendation engine: computes job match scores using cosine similarity
over binary skill vectors, detects missing skills, and maps missing
skills to recommended courses.
"""
from typing import List, Set, Tuple
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User
from app.models.course import Course


def cosine_similarity(vec_a: List[int], vec_b: List[int]) -> float:
    """Pure cosine similarity between two equal-length binary vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_skill_vectors(
    user_skill_ids: Set[int], job_skill_ids: Set[int]
) -> Tuple[List[int], List[int]]:
    """Builds binary presence vectors over the union of both skill ID sets."""
    all_skill_ids = sorted(user_skill_ids | job_skill_ids)
    user_vec = [1 if sid in user_skill_ids else 0 for sid in all_skill_ids]
    job_vec = [1 if sid in job_skill_ids else 0 for sid in all_skill_ids]
    return user_vec, job_vec


def compute_missing_skill_ids(
    user_skill_ids: Set[int], job_skill_ids: Set[int]
) -> Set[int]:
    """Skills required by the job but absent from the user's skill set."""
    return job_skill_ids - user_skill_ids


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
    For the current user, scores every job by cosine similarity of skill
    vectors, finds missing skills, and attaches course recommendations.
    Returns results sorted by match_score descending.
    """
    user_skill_ids = {s.id for s in current_user.skills}
    jobs = db.query(Job).all()
    results = []

    for job in jobs:
        job_skill_ids = {s.id for s in job.skills}
        if not job_skill_ids:
            continue

        user_vec, job_vec = build_skill_vectors(user_skill_ids, job_skill_ids)
        score = cosine_similarity(user_vec, job_vec)

        missing_ids = compute_missing_skill_ids(user_skill_ids, job_skill_ids)
        missing_skills = (
            db.query(Skill).filter(Skill.id.in_(missing_ids)).all()
            if missing_ids
            else []
        )
        courses = recommend_courses_for_skills(missing_ids, db)

        results.append({
            "job_id": job.id,
            "job": job,
            "user_id": current_user.id,
            "match_score": round(score, 4),
            "missing_skills": [s.name for s in missing_skills],
            "recommended_courses": [
                {"title": c.title, "provider": c.provider, "url": c.url}
                for c in courses
            ],
        })

    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results