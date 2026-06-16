import pytest
from pydantic import ValidationError
from models.schemas import AppointmentCreate

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "valid_postcode",
    [
        "SW1A 1AA",
        "ec1a 1bb",
        "W1A0AX",
        "M11AE",
        "B33 8TH",
        "CR2 6XH",
        "DN55 1PT",
        "GIR0AA",
        " gir 0aa ",  # spaces and casing variations
        "SW1A1AA",
    ],
)
def test_valid_postcodes(valid_postcode):
    appt = AppointmentCreate(
        date="2028-01-01",
        time="10:00",
        insect_id=1,
        door_number="1",
        road_name="Valid Road",
        postcode=valid_postcode,
    )
    # The postcode is cleaned (uppercased, spaces removed)
    expected_cleaned = valid_postcode.upper().replace(" ", "").strip()
    assert appt.postcode == expected_cleaned


@pytest.mark.parametrize(
    "invalid_postcode",
    [
        "SW1A 1AAinvalid",
        "M11AEextra",
        "GIR0AAabc",
        "invalidSW1A1AA",
        "12345",
        "ABCDEFG",
        "SW1A1A",
        "SW1A1AAA",
        "SW1A 1A",
        "GIR0A",
        "GIR0AAA",
        "",
        "   ",
    ],
)
def test_invalid_postcodes(invalid_postcode):
    with pytest.raises(ValidationError) as exc_info:
        AppointmentCreate(
            date="2028-01-01",
            time="10:00",
            insect_id=1,
            door_number="1",
            road_name="Valid Road",
            postcode=invalid_postcode,
        )
    assert "Invalid UK Postcode structure" in str(exc_info.value)
