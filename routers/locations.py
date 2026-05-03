from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.database import ServiceLocation
from models.schemas import LocationResponse
from dependencies.dbclients import get_db

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    return db.query(ServiceLocation).all()
