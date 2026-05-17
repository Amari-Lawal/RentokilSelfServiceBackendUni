"""User repository implementation with interface."""

from abc import ABC, abstractmethod
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.database import User
from models.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


class UserRepository(IUserRepository):
    """Concrete implementation of IUserRepository."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate, is_admin: bool = False):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username, password_hash=hashed_password, is_admin=is_admin
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
