from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base

import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# If it's a postgres URL from Heroku or similar, it might start with postgres://
# SQLAlchemy 1.4+ requires postgresql://
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # check_same_thread is only needed for SQLite
    connect_args={"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from models.database import User
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        admin = db.query(User).filter(User.username == "admin").first()
        hashed_pw = pwd_context.hash("adminpassword123")
        if not admin:
            admin_user = User(username="admin", password_hash=hashed_pw, is_admin=True)
            db.add(admin_user)
        else:
            # For POC, ensure password and admin status are reset to default
            admin.password_hash = hashed_pw
            admin.is_admin = True

        # Seed Insects
        from models.database import Insect

        if db.query(Insect).count() == 0:
            sample_insects = [
                Insect(
                    name="Ants",
                    description="Common garden ants and carpenter ants.",
                    danger_level=1,
                ),
                Insect(
                    name="Bed Bugs",
                    description="Parasitic insects that feed on blood.",
                    danger_level=3,
                ),
                Insect(
                    name="Cockroaches",
                    description="Resilient pests carrying bacteria.",
                    danger_level=3,
                ),
                Insect(
                    name="Termites",
                    description="Structural pests that destroy wood.",
                    danger_level=4,
                ),
                Insect(
                    name="Rodents",
                    description="Mice and rats that can carry diseases.",
                    danger_level=4,
                ),
                Insect(
                    name="Wasps/Bees",
                    description="Stinging insects that can cause allergic reactions.",
                    danger_level=2,
                ),
                Insect(
                    name="Other",
                    description="Miscellaneous pest types.",
                    danger_level=1,
                ),
            ]
            db.add_all(sample_insects)

        # Seed Locations
        from models.database import ServiceLocation

        if db.query(ServiceLocation).count() == 0:
            sample_locations = [
                ServiceLocation(
                    name="London Central", region="Greater London", postcode_prefix="EC"
                ),
                ServiceLocation(
                    name="Enfield", region="North London", postcode_prefix="EN"
                ),
                ServiceLocation(
                    name="Manchester", region="North West", postcode_prefix="M"
                ),
                ServiceLocation(
                    name="Birmingham", region="West Midlands", postcode_prefix="B"
                ),
                ServiceLocation(name="Leeds", region="Yorkshire", postcode_prefix="LS"),
                ServiceLocation(name="Glasgow", region="Scotland", postcode_prefix="G"),
            ]
            db.add_all(sample_locations)

        db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
