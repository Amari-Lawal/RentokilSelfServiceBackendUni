from fastapi import APIRouter, Depends
from typing import List
from models.schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from services.AppointmentService import AppointmentService
from models.database import User
from dependencies.services import get_appointment_service, get_current_user

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    current_user: User = Depends(get_current_user),
    appt_service: AppointmentService = Depends(get_appointment_service),
):
    if current_user.is_admin:
        return appt_service.get_all_appointments()
    return appt_service.get_user_appointments(current_user.id)


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    appt_service: AppointmentService = Depends(get_appointment_service),
):
    return appt_service.create_appointment(current_user.id, appointment)


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    appt_service: AppointmentService = Depends(get_appointment_service),
):
    return appt_service.update_appointment(appointment_id, appointment, current_user)


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    appt_service: AppointmentService = Depends(get_appointment_service),
):
    success = appt_service.delete_appointment(appointment_id, current_user)
    return {"success": success}
