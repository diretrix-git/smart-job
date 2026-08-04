from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.schemas.recommendation import RecommendationOut
from app.services.recommender import calculate_job_matches

router = APIRouter()

@router.get("/jobs", response_model=List[RecommendationOut])
def get_job_recommendations(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns job recommendations for the user.
    """
    return calculate_job_matches(db, current_user)

@router.get("/courses")
def get_course_recommendations(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns course recommendations for the user's skill gaps.
    """
    return {"message": "Recommendation engine course endpoint stub."}
