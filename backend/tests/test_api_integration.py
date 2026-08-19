from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime

from app.main import app
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.job import Job
from app.models.skill import Skill

client = TestClient(app)

def test_get_job_recommendations():
    # Real ORM instances so Pydantic serialization doesn't crash on MagicMocks
    mock_skill = Skill(id=1, name="Python", category="Programming")
    mock_job = Job(id=10, title="Backend Dev", description="Test desc", company="Tech", created_at=datetime.utcnow())
    
    mock_js = MagicMock()
    mock_js.skill_id = mock_skill.id
    mock_js.skill = mock_skill
    mock_js.importance = "required"
    mock_job.job_skills = [mock_js]
    
    mock_user = User(id=1, email="test@test.com", password_hash="dummy")
    mock_user.skills = [mock_skill]
    mock_user.resumes = []

    # Mock DB Session
    mock_db = MagicMock()
    mock_db.query.return_value.all.return_value = [mock_job]
    mock_db.query.return_value.filter.return_value.all.return_value = []
    mock_db.query.return_value.join.return_value.filter.return_value.distinct.return_value.all.return_value = []

    # Override dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db

    # Test endpoint
    response = client.get("/api/v1/recommendations/jobs")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["job_id"] == 10
    assert data[0]["match_score"] == 0.6
    assert data[0]["user_id"] == 1
    assert data[0]["job"]["title"] == "Backend Dev"
