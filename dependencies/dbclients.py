from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
            admin_user = User(
                username="admin",
                password_hash=hashed_pw,
                is_admin=True
            )
            db.add(admin_user)
        else:
            # For POC, ensure password and admin status are reset to default
            admin.password_hash = hashed_pw
            admin.is_admin = True
        db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
