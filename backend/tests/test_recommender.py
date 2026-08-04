from unittest.mock import MagicMock

from app.services.recommender import (
    cosine_similarity,
    build_skill_vectors,
    compute_missing_skill_ids,
    calculate_job_matches,
)


def test_cosine_similarity_identical_vectors():
    assert round(cosine_similarity([1, 1, 0], [1, 1, 0]), 4) == 1.0


def test_cosine_similarity_orthogonal_vectors():
    assert cosine_similarity([1, 0], [0, 1]) == 0.0


def test_cosine_similarity_partial_overlap():
    score = cosine_similarity([1, 1, 0], [1, 0, 0])
    assert round(score, 4) == round(1 / (2 ** 0.5), 4)


def test_cosine_similarity_empty_vector_returns_zero():
    assert cosine_similarity([0, 0], [1, 1]) == 0.0


def test_cosine_similarity_mismatched_length_raises():
    try:
        cosine_similarity([1, 0], [1, 0, 0])
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_build_skill_vectors_union_length():
    user_ids = {1, 2}
    job_ids = {2, 3}
    user_vec, job_vec = build_skill_vectors(user_ids, job_ids)
    assert len(user_vec) == 3
    assert len(job_vec) == 3
    assert sum(user_vec) == 2
    assert sum(job_vec) == 2


def test_compute_missing_skill_ids():
    user_ids = {1, 2}
    job_ids = {2, 3, 4}
    missing = compute_missing_skill_ids(user_ids, job_ids)
    assert missing == {3, 4}


def test_compute_missing_skill_ids_no_gap():
    user_ids = {1, 2, 3}
    job_ids = {1, 2}
    assert compute_missing_skill_ids(user_ids, job_ids) == set()


def _make_skill(skill_id, name):
    skill = MagicMock()
    skill.id = skill_id
    skill.name = name
    return skill


def _make_job(job_id, skills):
    job = MagicMock()
    job.id = job_id
    job.skills = skills
    return job


def test_calculate_job_matches_scores_and_sorts():
    python_skill = _make_skill(1, "Python")
    sql_skill = _make_skill(2, "SQL")
    docker_skill = _make_skill(3, "Docker")

    user = MagicMock()
    user.id = 4
    user.skills = [python_skill]

    job_high_match = _make_job(10, [python_skill])
    job_low_match = _make_job(11, [python_skill, sql_skill, docker_skill])

    db = MagicMock()
    db.query.return_value.all.return_value = [job_high_match, job_low_match]
    db.query.return_value.filter.return_value.all.return_value = [docker_skill, sql_skill]
    db.query.return_value.join.return_value.filter.return_value.distinct.return_value.all.return_value = []

    results = calculate_job_matches(db, user)

    assert len(results) == 2
    assert results[0]["job_id"] == 10
    assert results[0]["match_score"] == 1.0
    assert results[1]["job_id"] == 11
    assert results[1]["match_score"] < 1.0