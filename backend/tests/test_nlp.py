"""
Unit tests for nlp_extractor.py. Uses the real spaCy model since
PhraseMatcher depends on a live nlp.vocab, mocking it would not
test real matching behavior.
"""
from unittest.mock import MagicMock

from app.services.nlp_extractor import (
    nlp,
    load_skill_matcher,
    extract_skills_from_text,
)
from spacy.matcher import PhraseMatcher


def _make_skill(skill_id, name):
    skill = MagicMock()
    skill.id = skill_id
    skill.name = name
    return skill


def _build_matcher_from_skills(skills):
    """Helper mirroring load_skill_matcher's logic without a real DB."""
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for skill in skills:
        pattern = nlp.make_doc(skill.name)
        matcher.add(str(skill.id), [pattern])
    return matcher


def test_load_skill_matcher_builds_matcher_from_db_skills():
    skills = [_make_skill(1, "Python"), _make_skill(2, "SQL")]
    db = MagicMock()
    db.query.return_value.all.return_value = skills

    matcher = load_skill_matcher(db)

    assert isinstance(matcher, PhraseMatcher)
    assert len(matcher) == 2


def test_extract_skills_finds_exact_match():
    skills = [_make_skill(1, "Python")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("I am an experienced Python developer.", matcher)

    assert result == [1]


def test_extract_skills_is_case_insensitive():
    skills = [_make_skill(1, "python")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("I know PYTHON very well.", matcher)

    assert result == [1]


def test_extract_skills_finds_multiple_distinct_skills():
    skills = [_make_skill(1, "Python"), _make_skill(2, "SQL")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("Skilled in Python and SQL.", matcher)

    assert sorted(result) == [1, 2]


def test_extract_skills_returns_empty_list_for_no_match():
    skills = [_make_skill(1, "Kubernetes")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("I like cooking and painting.", matcher)

    assert result == []


def test_extract_skills_deduplicates_repeated_mentions():
    skills = [_make_skill(1, "Python")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("Python Python Python developer.", matcher)

    assert result == [1]


def test_extract_skills_handles_multi_word_skill_names():
    skills = [_make_skill(1, "Machine Learning")]
    matcher = _build_matcher_from_skills(skills)

    result = extract_skills_from_text("Experience with Machine Learning models.", matcher)

    assert result == [1]