from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, date as date_type


# Users
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


# Insects
class InsectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    danger_level: int

    class Config:
        from_attributes = True


# Locations
class LocationResponse(BaseModel):
    id: int
    name: str
    region: str

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    date: str
    time: str
    insect_id: int
    door_number: str
    road_name: str
    postcode: str
    notes: Optional[str] = None

    @field_validator("door_number")
    @classmethod
    def door_number_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Door number cannot be empty")
        if len(v.strip()) > 10:
            raise ValueError("Door number is too long (max 10 chars)")
        return v.strip()

    @field_validator("postcode")
    @classmethod
    def postcode_must_be_uk(cls, v: str) -> str:
        import re

        # Official UK Postcode Structural Regex (No Spaces)
        uk_regex = r"^(([A-Z]{1,2}[0-9][A-Z0-9]?)([0-9][A-Z]{2}))|(GIR0AA)$"
        if not re.match(uk_regex, v.upper().strip()):
            raise ValueError(
                "Invalid UK Postcode structure. Please use the no-space format."
            )
        return v.upper().strip()

    @field_validator("date")
    @classmethod
    def date_must_be_future(cls, v: str) -> str:
        try:
            input_date = datetime.strptime(v, "%Y-%m-%d").date()
            if input_date < date_type.today():
                raise ValueError("Appointment date cannot be in the past")
        except ValueError as e:
            if "Appointment date cannot be in the past" in str(e):
                raise e
            raise ValueError("Invalid date format, use YYYY-MM-DD")
        return v


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    insect_id: Optional[int] = None
    location_id: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int
    creator_username: Optional[str] = None
    insect: Optional[InsectResponse] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
