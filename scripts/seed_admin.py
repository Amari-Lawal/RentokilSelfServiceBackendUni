import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from dependencies.dbclients import SessionLocal, engine
from models.database import Base, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Seeding initial admin user...")
            hashed_pw = pwd_context.hash("adminpassword123")
            admin_user = User(
                username="admin",
                password_hash=hashed_pw,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created: admin / adminpassword123")
        else:
            print("Admin user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
