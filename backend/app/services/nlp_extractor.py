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

from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize sentence-transformers model globally
try:
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading sentence-transformers model: {e}")
    semantic_model = None

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

def compute_semantic_score(resume_raw_text: str, job_description: str) -> float:
    """
    Computes cosine similarity between resume and job description using sentence-transformers.
    Returns a score between 0.0 and 1.0.
    """
    if not resume_raw_text or not resume_raw_text.strip():
        return 0.0
    if not job_description or not job_description.strip():
        return 0.0
    if semantic_model is None:
        return 0.0
        
    embeddings = semantic_model.encode([resume_raw_text, job_description])
    
    # Compute cosine similarity
    vec_a = embeddings[0]
    vec_b = embeddings[1]
    
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(dot / (norm_a * norm_b))
