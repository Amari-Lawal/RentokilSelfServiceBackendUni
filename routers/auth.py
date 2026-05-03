from fastapi import APIRouter, Depends
from models.schemas import UserCreate, UserLogin, UserResponse, Token
from services.AuthService import AuthService
from dependencies.services import get_auth_service, get_current_admin_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register(user)


@router.post("/create-admin", response_model=UserResponse)
def create_admin(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    current_admin: UserResponse = Depends(get_current_admin_user),
):
    return auth_service.create_admin(user)


@router.post("/login", response_model=Token)
def login(user: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.authenticate(user)
