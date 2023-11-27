from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from model.models import User
from model.schemas import UserCreate


def register(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )
    user = User(email=user_data.email)
    db.add(user)
    db.commit()
    return user

