from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from model import schemas
from views.users import get_users
from model.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users
