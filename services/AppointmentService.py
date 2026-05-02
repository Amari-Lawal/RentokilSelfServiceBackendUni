from repository.AppointmentRepository import AppointmentRepository
from models.schemas import AppointmentCreate, AppointmentUpdate
from fastapi import HTTPException

class AppointmentService:
    def __init__(self, appt_repo: AppointmentRepository):
        self.appt_repo = appt_repo

    def get_user_appointments(self, user_id: int):
        return self.appt_repo.get_appointments_by_user(user_id)

    def get_all_appointments(self):
        return self.appt_repo.get_all_appointments()

    def create_appointment(self, user_id: int, appt_data: AppointmentCreate):
        return self.appt_repo.create_appointment(user_id, appt_data)

    def update_appointment(self, appt_id: int, appt_data: AppointmentUpdate, user):
        appt = self.appt_repo.get_appointment(appt_id)
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Only admin or the owner can update
        if not user.is_admin and appt.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this appointment")
            
        return self.appt_repo.update_appointment(appt_id, appt_data)

    def delete_appointment(self, appt_id: int, user):
        appt = self.appt_repo.get_appointment(appt_id)
        if not appt:
            raise HTTPException(status_code=404, detail="Appointment not found")
            
        # Only admin or the owner can delete
        if not user.is_admin and appt.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this appointment")
            
        return self.appt_repo.delete_appointment(appt_id)
