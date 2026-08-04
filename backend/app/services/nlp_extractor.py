import spacy
from spacy.matcher import PhraseMatcher
from typing import List
from sqlalchemy.orm import Session
from app.models.skill import Skill

# Initialize spaCy model globally to avoid reloading overhead per request
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model is not downloaded yet
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def load_skill_matcher(db: Session) -> PhraseMatcher:
    """
    Loads all skills from the DB into a spaCy PhraseMatcher.
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    skills = db.query(Skill).all()
    
    for skill in skills:
        pattern = nlp.make_doc(skill.name)
        # Using the skill ID as the match_id string
        matcher.add(str(skill.id), [pattern])
        
    return matcher

def extract_skills_from_text(text: str, matcher: PhraseMatcher) -> List[int]:
    """
    Given a raw text and a populated PhraseMatcher,
    returns a unique list of matched skill IDs.
    """
    doc = nlp(text)
    matches = matcher(doc)
    
    # matches returns a list of tuples: (match_id, start, end)
    skill_ids = set()
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        skill_ids.add(int(string_id))
        
    return list(skill_ids)
