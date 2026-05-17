"""Interface for AuthService."""

from abc import ABC, abstractmethod
from models.schemas import UserCreate, UserLogin


class IAuthService(ABC):
    """Interface for AuthService."""

    @abstractmethod
    def register(self, user_data: UserCreate):
        pass

    @abstractmethod
    def create_admin(self, user_data: UserCreate):
        pass

    @abstractmethod
    def authenticate(self, user_data: UserLogin):
        pass

    @abstractmethod
    def get_current_user(self, token: str):
        pass
