"""Interface for AppointmentService."""

from abc import ABC, abstractmethod
from models.schemas import AppointmentCreate, AppointmentUpdate


class IAppointmentService(ABC):
    """Interface for AppointmentService."""

    @abstractmethod
    def get_user_appointments(self, user_id: int):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass

    @abstractmethod
    def create_appointment(self, user_id: int, appt_data: AppointmentCreate):
        pass

    @abstractmethod
    def update_appointment(self, appt_id: int, appt_data: AppointmentUpdate, user):
        pass

    @abstractmethod
    def delete_appointment(self, appt_id: int, user):
        pass
