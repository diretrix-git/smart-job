from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeOut, ExtractedSkills
from app.services.pdf_parser import parse_pdf_from_bytes
from app.services.nlp_extractor import load_skill_matcher, extract_skills_from_text

router = APIRouter()

@router.post("/upload", response_model=ResumeOut)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    file_bytes = await file.read()
    try:
        raw_text = parse_pdf_from_bytes(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
        
    # Store the resume
    db_resume = Resume(user_id=current_user.id, raw_text=raw_text)
    db.add(db_resume)
    
    # Extract skills
    matcher = load_skill_matcher(db)
    skill_ids = extract_skills_from_text(raw_text, matcher)
    
    # Update user's skills
    current_user.skills.clear()
    
    from app.models.skill import Skill
    matched_skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
    for skill in matched_skills:
        current_user.skills.append(skill)
        
    db.commit()
    db.refresh(db_resume)
    
    return db_resume

@router.get("/skills", response_model=ExtractedSkills)
def get_user_skills(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    skill_names = [skill.name for skill in current_user.skills]
    return {"skills": skill_names}
