from sqlalchemy.orm import Session
from models.database import Appointment
from models.schemas import AppointmentCreate, AppointmentUpdate

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_appointment(self, appointment_id: int):
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_appointments_by_user(self, user_id: int):
        return self.db.query(Appointment).filter(Appointment.user_id == user_id).all()

    def get_all_appointments(self):
        return self.db.query(Appointment).all()

    def create_appointment(self, user_id: int, appointment: AppointmentCreate):
        db_appointment = Appointment(
            user_id=user_id,
            **appointment.model_dump()
        )
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def update_appointment(self, appointment_id: int, appointment: AppointmentUpdate):
        db_appointment = self.get_appointment(appointment_id)
        if db_appointment:
            update_data = appointment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_appointment, key, value)
            self.db.commit()
            self.db.refresh(db_appointment)
        return db_appointment

    def delete_appointment(self, appointment_id: int):
        db_appointment = self.get_appointment(appointment_id)
        if db_appointment:
            self.db.delete(db_appointment)
            self.db.commit()
            return True
        return False
