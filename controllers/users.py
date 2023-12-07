from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models.model import User
from models.schemas import UserCreate
from auth import pwd_context
from views.users import get_user


def register_user(db: Session, user_data: UserCreate):
    if db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )
    user = User(email=user_data.email)
    user.hashed_password = pwd_context.hash(user_data.password)
    db.add(user)
    db.commit()
    return {
        "id": user.id,
        "email": user.email,
    }


def delete_user(access_token: str, db: Session):
    user = get_user(access_token=access_token, db=db)
    db.delete(user)
    db.commit()
