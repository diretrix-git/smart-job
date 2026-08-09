from unittest.mock import MagicMock, patch

from app.services.recommender import (
    cosine_similarity,
    build_skill_vectors,
    calculate_job_matches,
)
from app.core.config import settings


def test_cosine_similarity_identical_vectors():
    assert round(cosine_similarity([1.0, 1.0, 0.0], [1.0, 1.0, 0.0]), 4) == 1.0


def test_cosine_similarity_orthogonal_vectors():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_cosine_similarity_partial_overlap():
    score = cosine_similarity([1.0, 1.0, 0.0], [1.0, 0.0, 0.0])
    assert round(score, 4) == round(1.0 / (2.0 ** 0.5), 4)


def test_cosine_similarity_empty_vector_returns_zero():
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_build_skill_vectors_weighted():
    user_ids = {1, 2}
    job_skills = {2: "required", 3: "preferred"}
    user_vec, job_vec = build_skill_vectors(user_ids, job_skills)
    
    assert len(user_vec) == 3
    assert len(job_vec) == 3
    # user_vec has 1 for skill 1 and 2
    assert user_vec == [1.0, 1.0, 0.0]
    # job_vec has required for 2, preferred for 3, missing for 1
    assert job_vec == [0.0, 1.0, 0.5]


def _make_skill(skill_id, name):
    skill = MagicMock()
    skill.id = skill_id
    skill.name = name
    return skill


def _make_job(job_id, skills, importances=None):
    if importances is None:
        importances = ["required"] * len(skills)
    job = MagicMock()
    job.id = job_id
    job.description = "Test description"
    job_skills_list = []
    for skill, imp in zip(skills, importances):
        js = MagicMock()
        js.skill_id = skill.id
        js.skill = skill
        js.importance = imp
        job_skills_list.append(js)
    job.job_skills = job_skills_list
    return job


@patch('app.services.recommender.compute_semantic_score')
def test_calculate_job_matches_scores_and_sorts(mock_semantic):
    mock_semantic.return_value = 0.5 # constant semantic score
    
    python_skill = _make_skill(1, "Python")
    sql_skill = _make_skill(2, "SQL")
    docker_skill = _make_skill(3, "Docker")

    user = MagicMock()
    user.id = 4
    user.skills = [python_skill]
    
    resume = MagicMock()
    resume.raw_text = "I am a Python developer."
    resume.uploaded_at = "2023-01-01"
    user.resumes = [resume]

    job_high_match = _make_job(10, [python_skill])
    job_low_match = _make_job(11, [python_skill, sql_skill, docker_skill], ["required", "preferred", "required"])

    db = MagicMock()
    db.query.return_value.all.return_value = [job_high_match, job_low_match]
    db.query.return_value.join.return_value.filter.return_value.distinct.return_value.all.return_value = []

    results = calculate_job_matches(db, user)

    assert len(results) == 2
    
    # 10 is higher match than 11
    assert results[0]["job_id"] == 10
    
    # Check job 10 (perfect skill match)
    assert results[0]["skill_score"] == 1.0
    expected_final_10 = (settings.SKILL_WEIGHT * 1.0) + (settings.SEMANTIC_WEIGHT * 0.5)
    assert results[0]["final_score"] == round(expected_final_10, 4)
    
    # Check job 11
    assert results[1]["job_id"] == 11
    assert results[1]["skill_score"] < 1.0
    
    assert "Python" in results[1]["matched_required_skills"]
    assert "SQL" in results[1]["missing_preferred_skills"]
    assert "Docker" in results[1]["missing_required_skills"]


def test_semantic_score_empty_text():
    from app.services.nlp_extractor import compute_semantic_score
    # Should return 0.0 for empty
    assert compute_semantic_score("", "description") == 0.0
    assert compute_semantic_score("resume", "") == 0.0


def test_semantic_score_real():
    from app.services.nlp_extractor import compute_semantic_score
    score1 = compute_semantic_score("Python developer", "Looking for a Python developer")
    score2 = compute_semantic_score("Python developer", "Looking for a chef")
    assert score1 > score2