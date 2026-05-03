from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.database import Insect
from models.schemas import InsectResponse
from dependencies.dbclients import get_db

router = APIRouter(prefix="/insects", tags=["insects"])


@router.get("/", response_model=List[InsectResponse])
def get_insects(db: Session = Depends(get_db)):
    return db.query(Insect).all()
