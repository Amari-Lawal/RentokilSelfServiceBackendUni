import os
from fastapi import APIRouter, Depends, Response
from models.schemas import UserCreate, UserLogin, UserResponse, Token
from services.AuthService import AuthService
from dependencies.services import get_auth_service, get_current_admin_user

router = APIRouter(prefix="/auth", tags=["auth"])

# Detect environment for cookie security
ENV = os.getenv("ENVIRONMENT", "development")
IS_PROD = ENV != "development"


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
def login(
    user: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    token_data = auth_service.authenticate(user)
    response.set_cookie(
        key="access_token",
        value=token_data.access_token,
        httponly=True,
        secure=IS_PROD,
        samesite="none" if IS_PROD else "lax",
    )
    return token_data


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=IS_PROD,
        samesite="none" if IS_PROD else "lax",
    )
    return {"message": "Logged out successfully"}
