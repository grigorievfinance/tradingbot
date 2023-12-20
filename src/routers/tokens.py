from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.tokens import create_user_token
from src.models import schemas
from src.models.database import get_db

router = APIRouter()


@router.post("", response_model=schemas.Token, status_code=201)
def create_token(user_data: schemas.UserAuth, db: Session = Depends(get_db)):
    return create_user_token(db=db, user_data=user_data)
