from sqlalchemy.orm import Session
from models.database import Appointment
from models.schemas import AppointmentCreate, AppointmentUpdate


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_appointment(self, appointment_id: int):
        appt = (
            self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        )
        return self._attach_username(appt)

    def _attach_username(self, appt):
        if appt and appt.user:
            appt.creator_username = appt.user.username
        return appt

    def get_appointments_by_user(self, user_id: int):
        appts = self.db.query(Appointment).filter(Appointment.user_id == user_id).all()
        return [self._attach_username(a) for a in appts]

    def get_all_appointments(self):
        appts = self.db.query(Appointment).all()
        return [self._attach_username(a) for a in appts]

    def create_appointment(self, user_id: int, appointment: AppointmentCreate):
        db_appointment = Appointment(user_id=user_id, **appointment.model_dump())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return self._attach_username(db_appointment)

    def update_appointment(self, appointment_id: int, appointment: AppointmentUpdate):
        db_appointment = self.get_appointment(appointment_id)
        if db_appointment:
            update_data = appointment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_appointment, key, value)
            self.db.commit()
            self.db.refresh(db_appointment)
        return self._attach_username(db_appointment)

    def delete_appointment(self, appointment_id: int):
        db_appointment = self.get_appointment(appointment_id)
        if db_appointment:
            self.db.delete(db_appointment)
            self.db.commit()
            return True
        return False
