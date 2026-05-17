"""Interface for UserRepository."""

from abc import ABC, abstractmethod
from models.schemas import UserCreate


class IUserRepository(ABC):
    """Interface for UserRepository."""

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    def get_user(self, user_id: int):
        pass

    @abstractmethod
    def create_user(self, user: UserCreate, is_admin: bool = False):
        pass

    @abstractmethod
    def verify_password(self, plain_password, hashed_password):
        pass
