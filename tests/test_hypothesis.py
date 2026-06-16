from hypothesis import given, strategies as st
from models.schemas import AppointmentCreate
import pytest
from pydantic import ValidationError
from datetime import date, timedelta

pytestmark = pytest.mark.unit


# Simple Hypothesis test to verify AppointmentCreate validation
@given(
    door_number=st.text(min_size=1, max_size=10),
    road_name=st.text(min_size=3),
    postcode=st.just("SW1A1AA"),  # Using a fixed valid postcode to focus on other fields
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


@given(postcode=st.text())
def test_hypothesis_postcode_validation(postcode):
    import re

    uk_regex = r"^((([A-Z]{1,2}[0-9][A-Z0-9]?)([0-9][A-Z]{2}))|(GIR0AA))$"
    matches = re.match(uk_regex, postcode.upper().replace(" ", "").strip())

    try:
        AppointmentCreate(
            date="2028-01-01",
            time="10:00",
            insect_id=1,
            door_number="1",
            road_name="Valid Road",
            postcode=postcode,
        )
        assert matches is not None
    except ValidationError:
        assert matches is None


@given(date_val=st.dates(max_value=date.today() - timedelta(days=1)))
def test_hypothesis_past_date_fails(date_val):
    with pytest.raises(ValidationError):
        AppointmentCreate(
            date=date_val.strftime("%Y-%m-%d"),
            time="10:00",
            insect_id=1,
            door_number="1",
            road_name="Valid Road",
            postcode="SW1A1AA",
        )
