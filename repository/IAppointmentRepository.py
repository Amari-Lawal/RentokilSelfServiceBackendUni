"""Interface for AppointmentRepository."""

from abc import ABC, abstractmethod
from models.schemas import AppointmentCreate, AppointmentUpdate


class IAppointmentRepository(ABC):
    """Interface for AppointmentRepository."""

    @abstractmethod
    def get_appointment(self, appointment_id: int):
        pass

    @abstractmethod
    def get_appointments_by_user(self, user_id: int):
        pass

    @abstractmethod
    def get_all_appointments(self):
        pass

    @abstractmethod
    def create_appointment(self, user_id: int, appointment: AppointmentCreate):
        pass

    @abstractmethod
    def update_appointment(self, appointment_id: int, appointment: AppointmentUpdate):
        pass

    @abstractmethod
    def delete_appointment(self, appointment_id: int):
        pass
