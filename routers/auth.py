from fastapi import APIRouter, Depends
from models.schemas import UserCreate, UserLogin, UserResponse, Token
from services.AuthService import AuthService
from dependencies.services import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register(user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.authenticate(user)
