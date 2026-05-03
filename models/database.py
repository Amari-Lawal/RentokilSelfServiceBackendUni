from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    appointments = relationship(
        "Appointment", back_populates="user", cascade="all, delete-orphan"
    )


class Insect(Base):
    __tablename__ = "insects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    danger_level = Column(Integer, default=1)  # 1-5

    appointments = relationship("Appointment", back_populates="insect")


class ServiceLocation(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    region = Column(String, nullable=False)
    postcode_prefix = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insect_id = Column(Integer, ForeignKey("insects.id"), nullable=False)
    door_number = Column(String, nullable=False)
    road_name = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, default="Pending")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")
    insect = relationship("Insect", back_populates="appointments")
