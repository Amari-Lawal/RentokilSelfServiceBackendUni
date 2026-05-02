import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import Base
from dependencies.dbclients import engine, SessionLocal

# Setup test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_user():
    user_data = {
        "username": "testuser_crud",
        "password": "testpassword",
        "is_admin": False
    }
    # Create user
    response = client.post("/auth/register", json=user_data)
    if response.status_code == 400: # Already registered
        # Just login then
        login_res = client.post("/auth/login", json={"username": user_data["username"], "password": user_data["password"]})
        return login_res.json()
    else:
        assert response.status_code == 200
        # Login
        login_res = client.post("/auth/login", json={"username": user_data["username"], "password": user_data["password"]})
        return login_res.json()

def test_create_appointment(test_user):
    token = test_user["access_token"]
    appt_data = {
        "date": "2026-10-15",
        "time": "14:00",
        "insect_type": "Ants",
        "location": "456 Test Ave",
        "notes": "Testing crud"
    }
    response = client.post("/appointments/", json=appt_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["insect_type"] == "Ants"
    assert data["location"] == "456 Test Ave"
    assert "id" in data
    
    # Save id for other tests
    pytest.appt_id = data["id"]

def test_read_appointments(test_user):
    token = test_user["access_token"]
    response = client.get("/appointments/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(appt["id"] == pytest.appt_id for appt in data)

def test_update_appointment(test_user):
    token = test_user["access_token"]
    update_data = {
        "insect_type": "Bed Bugs"
    }
    response = client.put(f"/appointments/{pytest.appt_id}", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["insect_type"] == "Bed Bugs"
    # Status should remain Pending for regular users
    assert data["status"] == "Pending"

def test_delete_appointment(test_user):
    token = test_user["access_token"]
    response = client.delete(f"/appointments/{pytest.appt_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # Verify it's gone
    response = client.get("/appointments/", headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    assert not any(appt["id"] == pytest.appt_id for appt in data)
