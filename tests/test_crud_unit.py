from unittest.mock import MagicMock
import pytest
from repository.AppointmentRepository import AppointmentRepository
from models.schemas import AppointmentCreate
from models.database import Appointment, User

pytestmark = pytest.mark.unit


@pytest.fixture
def mock_db():
    return MagicMock()


def test_get_appointment(mock_db):
    repo = AppointmentRepository(mock_db)
    mock_appt = Appointment(id=1, user_id=1)
    mock_user = User(username="testuser")
    mock_appt.user = mock_user

    mock_db.query.return_value.filter.return_value.first.return_value = mock_appt

    result = repo.get_appointment(1)
    assert result.id == 1
    assert result.creator_username == "testuser"


def test_create_appointment(mock_db):
    repo = AppointmentRepository(mock_db)
    appt_data = AppointmentCreate(
        date="2026-10-15",
        time="14:00",
        insect_id=1,
        door_number="10",
        road_name="Test Lane",
        postcode="M11AA",
    )

    repo.create_appointment(user_id=1, appointment=appt_data)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
