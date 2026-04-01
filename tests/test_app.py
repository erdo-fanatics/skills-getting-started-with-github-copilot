from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # keep tests isolated by using a fresh copy of baseline data
    baseline = {
        name: {**data, "participants": data["participants"].copy()}
        for name, data in {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
            "Basketball Team": {
                "description": "Competitive basketball team and training",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 15,
                "participants": ["james@mergington.edu"],
            },
            "Tennis Club": {
                "description": "Tennis instruction and friendly matches",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
                "max_participants": 10,
                "participants": ["sarah@mergington.edu", "ryan@mergington.edu"],
            },
            "Art Studio": {
                "description": "Painting, drawing, and visual arts",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 18,
                "participants": ["emma@mergington.edu"],
            },
            "Music Band": {
                "description": "Learn instruments and perform in concerts",
                "schedule": "Mondays and Fridays, 4:00 PM - 5:00 PM",
                "max_participants": 25,
                "participants": ["lucas@mergington.edu", "isabella@mergington.edu"],
            },
            "Debate Team": {
                "description": "Develop public speaking and argumentation skills",
                "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
                "max_participants": 16,
                "participants": ["alex@mergington.edu"],
            },
            "Science Club": {
                "description": "Explore STEM topics and conduct experiments",
                "schedule": "Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 22,
                "participants": ["maya@mergington.edu", "carlos@mergington.edu"],
            },
        }.items()
    }
    activities.clear()
    activities.update(baseline)


def test_get_activities_returns_200_and_has_keys():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    target_email = "student1@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={target_email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert target_email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    target_email = "student2@mergington.edu"
    client.post(f"/activities/Chess%20Club/signup?email={target_email}")
    response = client.post(f"/activities/Chess%20Club/signup?email={target_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    existing_email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/unregister?email={existing_email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert existing_email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_400():
    missing_email = "missing@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/unregister?email={missing_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
