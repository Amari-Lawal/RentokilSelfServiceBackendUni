from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies.dbclients import get_db
from repository.UserRepository import UserRepository
from repository.AppointmentRepository import AppointmentRepository
from services.AuthService import AuthService
from services.AppointmentService import AppointmentService
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_appointment_repository(db: Session = Depends(get_db)):
    return AppointmentRepository(db)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)):
    return AuthService(user_repo)


def get_appointment_service(
    appt_repo: AppointmentRepository = Depends(get_appointment_repository),
):
    return AppointmentService(appt_repo)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.get_current_user(token)


def get_current_admin_user(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
