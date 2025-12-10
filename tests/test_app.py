import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    if response.status_code == 400:
        # Already signed up, so remove and try again
        from src.app import activities
        activities[activity]["participants"].remove(email)
        response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Ensure signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try duplicate
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
