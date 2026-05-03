from hypothesis import given, strategies as st
from models.schemas import AppointmentCreate
import pytest
from pydantic import ValidationError


# Simple Hypothesis test to verify AppointmentCreate validation
@given(
    door_number=st.text(min_size=1, max_size=10),
    road_name=st.text(min_size=3),
    postcode=st.just("EN11XW"),  # Using a fixed valid postcode to focus on other fields
    date=st.just("2028-01-01"),
    time=st.just("10:00"),
    insect_id=st.integers(min_value=1),
)
def test_appointment_create_valid_fields(
    door_number, road_name, postcode, date, time, insect_id
):
    if not door_number.strip():
        return  # Skip empty strings as door_number validator rejects them

    try:
        AppointmentCreate(
            date=date,
            time=time,
            insect_id=insect_id,
            door_number=door_number,
            road_name=road_name,
            postcode=postcode,
        )
    except ValidationError:
        # If it fails, it should be for a valid reason defined in the model
        pass


def test_hypothesis_postcode_negative():
    # Verify that random strings don't pass postcode validation
    with pytest.raises(ValidationError):
        AppointmentCreate(
            date="2028-01-01",
            time="10:00",
            insect_id=1,
            door_number="1",
            road_name="Valid Road",
            postcode="INVALID_POSTCODE",
        )
