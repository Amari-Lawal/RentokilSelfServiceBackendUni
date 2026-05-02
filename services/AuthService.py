from repository.UserRepository import UserRepository
from models.schemas import UserCreate, UserLogin
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, user_data: UserCreate):
        existing_user = self.user_repo.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return self.user_repo.create_user(user_data, is_admin=False)

    def create_admin(self, user_data: UserCreate):
        # This will be protected by an admin-only route in the router
        existing_user = self.user_repo.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
            
        return self.user_repo.create_user(user_data, is_admin=True)

    def authenticate(self, user_data: UserLogin):
        user = self.user_repo.get_user_by_username(user_data.username)
        if not user or not self.user_repo.verify_password(user_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + access_token_expires
        to_encode = {"sub": user.username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": encoded_jwt, 
            "token_type": "bearer",
            "user": user
        }

    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        user = self.user_repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
