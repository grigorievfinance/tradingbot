from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from models import schemas
from auth import apikey_scheme
from views.users import get_users, get_user
from models.database import get_db
from controllers.users import register_user, delete_user

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("", response_model=schemas.LiteUser, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register_user(db=db, user_data=user_data)


@router.get("/profile", response_model=schemas.LiteUser)
def get_user_by_token(access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    return get_user(access_token=access_token, db=db)


@router.delete("")
def delete(access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    delete_user(access_token=access_token, db=db)
