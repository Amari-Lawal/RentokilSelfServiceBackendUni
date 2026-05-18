"""Appointment service implementation."""

import logging
from fastapi import HTTPException
from repository.AppointmentRepository import AppointmentRepository
from models.schemas import AppointmentCreate, AppointmentUpdate
from services.IAppointmentService import IAppointmentService

logger = logging.getLogger(__name__)


class AppointmentService(IAppointmentService):
    """Concrete implementation of IAppointmentService."""

    def __init__(self, appt_repo: AppointmentRepository):
        self.appt_repo = appt_repo

    def get_user_appointments(self, user_id: int):
        return self.appt_repo.get_appointments_by_user(user_id)

    def get_all_appointments(self):
        return self.appt_repo.get_all_appointments()

    def create_appointment(self, user_id: int, appt_data: AppointmentCreate):
        appt = self.appt_repo.create_appointment(user_id, appt_data)
        logger.info(f"User {user_id} created appointment {appt.id}")
        return appt

    def update_appointment(self, appt_id: int, appt_data: AppointmentUpdate, user):
        appt = self.appt_repo.get_appointment(appt_id)
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")

        # Only admin or the owner can update
        if (
            "admin" not in [role.name for role in user.roles]
            and appt.user_id != user.id
        ):
            raise HTTPException(
                status_code=403, detail="Not authorized to update this appointment"
            )

        # RESTRICTIONS:
        update_dict = appt_data.model_dump(exclude_unset=True)

        if "admin" in [role.name for role in user.roles]:
            # Admin can ONLY update status
            restricted_data = {k: v for k, v in update_dict.items() if k == "status"}
            if not restricted_data:
                raise HTTPException(
                    status_code=400, detail="Admins can only update the status field"
                )
            return self.appt_repo.update_appointment(
                appt_id, AppointmentUpdate(**restricted_data)
            )

        # Regular user can update everything EXCEPT status
        if "status" in update_dict:
            del update_dict["status"]
        updated_appt = self.appt_repo.update_appointment(
            appt_id, AppointmentUpdate(**update_dict)
        )
        logger.info(f"User {user.id} updated appointment {appt_id}")
        return updated_appt

    def delete_appointment(self, appt_id: int, user):
        appt = self.appt_repo.get_appointment(appt_id)
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")

        # Only admin or the owner can delete
        if (
            "admin" not in [role.name for role in user.roles]
            and appt.user_id != user.id
        ):
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this appointment"
            )

        result = self.appt_repo.delete_appointment(appt_id)
        logger.info(f"User {user.id} deleted appointment {appt_id}")
        return result
