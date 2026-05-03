import pytest
from fastapi.testclient import TestClient
import time
from main import app
from models.database import Base
from dependencies.dbclients import engine

# Setup test database
Base.metadata.create_all(bind=engine)
client = TestClient(app)


@pytest.fixture
def user_token():
    # Register and login a regular user
    username = f"user_{int(time.time() * 1000)}"
    client.post("/auth/register", json={"username": username, "password": "password"})
    res = client.post(
        "/auth/login", json={"username": username, "password": "password"}
    )
    return res.json()["access_token"]


@pytest.fixture
def admin_token():
    # Use the seeded admin to create another admin for the test
    admin_login = client.post(
        "/auth/login", json={"username": "admin", "password": "adminpassword123"}
    )
    seed_token = admin_login.json()["access_token"]

    new_admin_name = f"test_admin_{int(time.time() * 1000)}"
    client.post(
        "/auth/create-admin",
        json={"username": new_admin_name, "password": "password"},
        headers={"Authorization": f"Bearer {seed_token}"},
    )

    res = client.post(
        "/auth/login", json={"username": new_admin_name, "password": "password"}
    )
    return res.json()["access_token"]


def test_user_cannot_update_status(user_token):
    # 1. Create appointment
    appt_data = {
        "date": "2027-01-01",
        "time": "10:00",
        "insect_id": 1,
        "door_number": "1",
        "road_name": "Main St",
        "postcode": "EC1A1BB",
    }
    res = client.post(
        "/appointments/",
        json=appt_data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    appt_id = res.json()["id"]

    # 2. Try to update status
    update_data = {"status": "Confirmed"}
    res = client.put(
        f"/appointments/{appt_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 200
    # Status should still be Pending because users can't change it
    assert res.json()["status"] == "Pending"


def test_admin_can_update_status_only(admin_token, user_token):
    # 1. User creates appointment
    appt_data = {
        "date": "2027-01-01",
        "time": "10:00",
        "insect_id": 1,
        "door_number": "1",
        "road_name": "Main St",
        "postcode": "EC1A1BB",
    }
    res = client.post(
        "/appointments/",
        json=appt_data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    appt_id = res.json()["id"]

    # 2. Admin updates status
    update_data = {"status": "Confirmed"}
    res = client.put(
        f"/appointments/{appt_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "Confirmed"

    # 3. Admin tries to update details (should be blocked)
    update_data = {"date": "2027-01-01"}
    res = client.put(
        f"/appointments/{appt_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 400
    assert "Admins can only update the status field" in res.json()["detail"]


def test_cross_user_access_blocked(user_token):
    # 1. User A (current user) creates appt
    # 2. Register User B
    user_b_name = f"user_b_{int(time.time() * 1000)}"
    client.post(
        "/auth/register", json={"username": user_b_name, "password": "password"}
    )
    res = client.post(
        "/auth/login", json={"username": user_b_name, "password": "password"}
    )
    token_b = res.json()["access_token"]

    appt_data = {
        "date": "2027-01-01",
        "time": "10:00",
        "insect_id": 1,
        "door_number": "1",
        "road_name": "Main St",
        "postcode": "EC1A1BB",
    }
    res = client.post(
        "/appointments/", json=appt_data, headers={"Authorization": f"Bearer {token_b}"}
    )
    appt_b_id = res.json()["id"]

    # 3. User A tries to update User B's appt
    res = client.put(
        f"/appointments/{appt_b_id}",
        json={"date": "2029-01-01"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 403
